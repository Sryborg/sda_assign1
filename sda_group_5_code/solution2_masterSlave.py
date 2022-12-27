from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

import time

def my_function(param1, param2, param3):
    result = param1 ** 2 * param2 + param3
    time.sleep(2)
    return result

params = np.random.random((15, 3)) * 100.0  
n = params.shape[0]

count = n // size
remainder = n % size

if rank < remainder:
    start = rank * (count + 1)
    stop = start + count + 1
else:
    start = rank * count + remainder
    stop = start + count

local_params = params[start:stop, :]
local_results = np.empty((local_params.shape[0], local_params.shape[1] + 1))
local_results[:, :local_params.shape[1]] = local_params
local_results[:, -1] = my_function(local_results[:, 0], local_results[:, 1], local_results[:, 2])


if rank > 0:
    comm.Send(local_results, dest=0, tag=14)
else:
    final_results = np.copy(local_results)
    for i in range(1, size):
        if i < remainder:
            rank_size = count + 1
        else:
            rank_size = count
        tmp = np.empty((rank_size, final_results.shape[1]), dtype=np.float)
        comm.Recv(tmp, source=i, tag=14)
        final_results = np.vstack((final_results, tmp))
    print("results")
    print(final_results)
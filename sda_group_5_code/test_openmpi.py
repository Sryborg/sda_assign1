from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
  print("Rank 0")
elif rank == 1:
  print ("Rank 1")
else:
  print("Not first or second rank")
    
print("Hello world from rank", str(rank), "of", str(size))


import time

def my_function(param1, param2, param3):
    result = param1 ** 2 * param2 + param3
    time.sleep(2)
    return result

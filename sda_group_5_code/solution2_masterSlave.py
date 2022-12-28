
################ Imports ####################
import time
from copy import deepcopy
import numpy as np
import pandas as pd
from mpi4py import MPI

################ Helper Functions ###############
def compute_results(list_of_dicts):
    list_of_dicts = list(list_of_dicts)
    result_total_profit = {}
    result_unit_sold = {}
    result_counts = {}
    for each_dict in list_of_dicts:
        # print(f"{each_dict=},\n {rank=}")
        if each_dict["region"] in result_total_profit:
            result_total_profit[each_dict["region"]] += each_dict["total_profit"]
            result_unit_sold[each_dict["region"]] += each_dict["units_sold"]
            result_counts[each_dict["region"]] += 1
        else:
            result_total_profit[each_dict["region"]] = each_dict["total_profit"]
            result_unit_sold[each_dict["region"]] = each_dict["units_sold"]
            result_counts[each_dict["region"]] = 1
    # print(f"{result_total_profit} \n {result_unit_sold} \n {result_counts}")
    return {"result_total_profit":result_total_profit, "result_unit_sold":result_unit_sold, "result_counts":result_counts}

################ Base Setup ###############
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

############### Reading Data ##############
main_df = pd.read_csv("geosales.csv")
list_of_records = main_df.to_dict('records')

############### Data Range Partition ##############
length_of_data = len(list_of_records)

local_params = np.array_split(list_of_records, size)

############### Send to Slaves ##############
scattered_data = comm.scatter(local_params, root=0)
scattered_data = compute_results(scattered_data)
# print('rank', rank, 'has data:', len(scattered_data))
############### Collect from slaves ##############
gathered_data = comm.gather(scattered_data, root=0)

############### Publish Result ##############
if rank == 0:
    total_profit = {}
    unit_sold = {}
    item_count = {}
    average_total_profits = {}
    # print(f"\n\n{gathered_data=}")
    for each_result in gathered_data:
        profit_dict = each_result["result_total_profit"]
        count_dict = each_result["result_counts"]
        unit_dict = each_result["result_unit_sold"]
        for key, value in profit_dict.items():
            if key in total_profit:
                total_profit[key] += value
                unit_sold[key] += unit_dict[key]
                item_count[key] += count_dict[key]
            else:
                total_profit[key] = value
                unit_sold[key] = unit_dict[key]
                item_count[key] = count_dict[key]
    
    for each_key, each_value in total_profit.items():
        average_total_profits[each_key] = each_value/item_count[each_key]
        print(f"""For "{each_key}" Region: Average Profit = {average_total_profits[each_key]} and Units Sold = {unit_sold[each_key]}""")
    # print("Result", total_profit, "\n", unit_sold, "\n", item_count, "\n", average_total_profits)







################ Old method | Please ignore ####################
# remainder = length_of_data % size
# count = length_of_data // size

# start = count*rank
# if rank == size - 1:
#     end = length_of_data
# else:
#     end = count*rank + count - 1
# print(f"{remainder=}, {count=}, {size=}, {rank=}, {start=}, {end=}, {length_of_data=}")


# local_params = list_of_records[start:end]
# local_results = [ {} for _ in range(size) ]
# local_results[rank] = compute_results(local_params, rank)


# local_results[:, :local_params.shape[1]] = local_params
# local_results[:, -1] = my_function(local_results[:, 0], local_results[:, 1], local_results[:, 2])

# if rank > 0:
#     comm.Send(local_results, dest=0, tag=14)
# else:
#     final_results = np.copy(local_results)
#     for i in range(1, size):
#         if i < remainder:
#             rank_size = count + 1
#         else:
#             rank_size = count
#         tmp = np.empty((rank_size, final_results.shape[1]), dtype=np.float)
#         comm.Recv(tmp, source=i, tag=14)
#         final_results = np.vstack((final_results, tmp))
#     print("results")
#     print(final_results)
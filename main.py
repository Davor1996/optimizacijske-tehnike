'''
W = 1000
v = [1..100]
t = [1..100]
broj predmeta 500

v/t poredati po vrednosti (obicni dantzig)

testirati performanse optimizovanog dantzinga s izbacivanjeg elemenata (ici redom pa probati izbaciti prvog pa provjeriti jel daje bolji rezultat, isto tako pokusati izbaciti samo 2. element, itd.
)

'''

import random
import time
import numpy as np

import algorithms.optimal_knapsack
import algorithms.greedy_knapsack
import algorithms.optimized_dantzing

# Variables
random_capacity = [1000, 1000]
random_values = [1, 100]
random_weights = [1, 100]
num_of_items = 500

# Setup
run_iterations = 10000
dantzig_optimal = 0
optimized_dantzig_better_cnt = 0
optimized_dantzig_optimal_cnt = 0
optimal_lenght = 0
greedy_lenght = 0
optimized_lenght = 0
all_optimized_optimal = 0
all_optimized_better = 0

optimal_list_time_solved = []
greedy_list_time_solved = []
optimized__list_time_solved = []

after_removing_xth_element_has_better_result = [0]*num_of_items
after_removing_xth_element_is_optimal = [0]*num_of_items
after_removing_xth_element_has_better_result_reversed = [0]*num_of_items
after_removing_xth_element_is_optimal_reversed = [0]*num_of_items


# Functions
def generate_random_items(rand_values, rand_weights, rand_capacity, len=10):
    items = []
    for i in range(len):
        items.append(
            (random.randint(rand_values[0], rand_values[1]), random.randint(rand_weights[0], rand_weights[1]))
        )

    capacity = random.randint(rand_capacity[0], rand_capacity[1])
    return items, capacity

def solve_given_knapsack(items, capacity, verbose=False):
    global dantzig_optimal, optimal_lenght, greedy_lenght, optimized_lenght, all_optimized_optimal, all_optimized_better, after_removing_xth_element_has_better_result, after_removing_xth_element_is_optimal, after_removing_xth_element_has_better_result_reversed, after_removing_xth_element_is_optimal_reversed
    #print(items)

    optimal_start = time.time_ns()
    optimal_value = algorithms.optimal_knapsack.solve_knapsack(items, capacity)
    optimal_end = time.time_ns()

    greedy_start = time.time_ns()
    greedy_knapsack, greedy_value, greedy_weight = algorithms.greedy_knapsack.solve_knapsack(items, capacity)
    greedy_lenght = greedy_lenght + len(greedy_knapsack)
    if greedy_value == optimal_value:
        dantzig_optimal = dantzig_optimal+1
    greedy_end = time.time_ns()

    
    # Verbose Results
    if verbose:
        print('-----------------[INFO]-----------------')
        print(f'Items: {items}')
        print(f'Knapsack capacity: {capacity}')

        print('\n-----------------[OPTIMAL]-----------------')
        print(f'Total value: {optimal_value}')

        print('\n-----------------[DANTZING]-----------------')
        print(f'Knapsack contents: {greedy_knapsack}')
        print(f'Total value: {greedy_value}')
        print(f'Total weight: {greedy_weight}')

        print('\n-----------------[OPTIMIZED DANTZING]-----------------')

    optimized_start = time.time_ns()
    optimized_lenght_iter = 0
    optimal = 0
    better = 0
    for i in range(len(greedy_knapsack)):
        optimized_knapsack, optimized_value, optimized_weight = algorithms.optimized_dantzing.solve_knapsack(items, capacity, i)
        optimized_lenght_iter = optimized_lenght_iter + len(optimized_knapsack)
        if optimized_value > greedy_value:
            better = better+1
            all_optimized_better = all_optimized_better+1
            after_removing_xth_element_has_better_result[i]=after_removing_xth_element_has_better_result[i]+1
            after_removing_xth_element_has_better_result_reversed[len(greedy_knapsack)-1-i]=after_removing_xth_element_has_better_result_reversed[len(greedy_knapsack)-1-i]+1
        if optimized_value == optimal_value:
            optimal = optimal+1
            all_optimized_optimal = all_optimized_optimal+1
            after_removing_xth_element_is_optimal[i]=after_removing_xth_element_is_optimal[i]+1
            after_removing_xth_element_is_optimal_reversed[len(greedy_knapsack)-1-i]=after_removing_xth_element_is_optimal_reversed[len(greedy_knapsack)-1-i]+1

        if verbose: #Will affect performance
            print(f'Element {i} removed')
            print(f'Knapsack contents: {optimized_knapsack}')
            print(f'Total value: {optimized_value}')
            print(f'Total weight: {optimized_weight}')

    if len(greedy_knapsack)>0:
        optimized_lenght = optimized_lenght + optimized_lenght_iter/len(greedy_knapsack)
    optimized_end = time.time_ns()


    if verbose:
        print('\n-----------------[RESULTS]-----------------')
        print(f'Optimized dantzing algorithm better than dantzing algorithm: {better}')
        print(f'Optimized dantzing algorithm optimal: {optimal}')
        print(f'--------------------------------------------')
    
    if len(greedy_knapsack)>0:
        return better, optimal, (optimal_end - optimal_start), (greedy_end - greedy_start), (optimized_end - optimized_start)/len(greedy_knapsack)
    else:
        return better, optimal, (optimal_end - optimal_start), (greedy_end - greedy_start), (optimized_end - optimized_start) #for division by zero



# Start testing

start = time.time_ns()
for i in range(run_iterations):
    print (f'Iteration: {i+1}')
    items, capacity = generate_random_items(random_values, random_weights, random_capacity, num_of_items)
    optimized_dantzig_better, optimized_dantzig_optimal, optimal_time_solved, greedy_time_solved, optimized_time_solved = solve_given_knapsack(items, capacity)

    optimal_list_time_solved.append(optimal_time_solved)
    greedy_list_time_solved.append(greedy_time_solved)
    optimized__list_time_solved.append(optimized_time_solved)

    if optimized_dantzig_better>0:
        optimized_dantzig_better_cnt += 1
    if optimized_dantzig_optimal>0:
        optimized_dantzig_optimal_cnt += 1


print('-----------------[RUN STATS]-----------------')
print(f'Run iterations: {run_iterations}')
print(f"Iterations in wich dantzig algorithm was optimal: {dantzig_optimal}")
print(f'Iterations in which optimized dantzig algorithm was better than dantzig algorithm: {optimized_dantzig_better_cnt}')
print(f'Iterations in which optimized dantzig algorithm was optimal: {optimized_dantzig_optimal_cnt}')
print(f"Iterations time: {(time.time_ns() - start) / 1e+6}ms")

print(f'Percentage in which optimized dantzig algorithm was better than dantzig alghoritm: {(optimized_dantzig_better_cnt / run_iterations) * 100}%')
print(f'Percentage in which optimized dantzig algorithm was optimal: {(optimized_dantzig_optimal_cnt / run_iterations) * 100}%' "\n")

print(f"all_optimized_optimal: {all_optimized_optimal}")
print(f"all_optimized_better: {all_optimized_better}")

print(f"-----------------[LIST LENGHT]-----------------")
print(f"Optimal lenght: {optimal_lenght/run_iterations}")
print(f"Greedy lenght: {greedy_lenght/run_iterations}")
print(f"Optimized lenght: {optimized_lenght/run_iterations}\n")

print(f"-----------------[AFTER REMOVING Xth ELEMENT]-----------------")
print(f"Better result: {after_removing_xth_element_has_better_result}")
print(f"Optimal result: {after_removing_xth_element_is_optimal}")
print(f"Better result reversed: {after_removing_xth_element_has_better_result_reversed}")
print(f"Optimal result reversed: {after_removing_xth_element_is_optimal_reversed}")

print(f"-----------------[TIME STATS]-----------------")
print(f"Optimal mean time: {np.mean(optimal_list_time_solved)}ns")
print(f"Greedy mean time: {np.mean(greedy_list_time_solved)}ns")
print(f"Optimized mean time: {np.mean(optimized__list_time_solved)}ns\n")

print(f"Optimal median time: {np.median(optimal_list_time_solved)}ns")
print(f"Greedy median time: {np.median(greedy_list_time_solved)}ns")
print(f"Optimized median time: {np.median(optimized__list_time_solved)}ns\n")

print(f"Optimal time sum: {np.sum(optimal_list_time_solved)}ns")
print(f"Greedy time sum: {np.sum(greedy_list_time_solved)}ns")
print(f"Optimized time sum: {np.sum(optimized__list_time_solved)}ns\n")

print(f"Optimized times: {(greedy_list_time_solved)}")

"""
    Solution to the 0/1 Knapsack problem using optimized Dantzing's greedy algorithm.
"""
import numpy as np

def solve_greedy_knapsack(items, capacity):
    items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)

    knapsack = []
    total_value = 0
    total_weight = 0

    for item in items:
        if total_weight + item[1] <= capacity:
            knapsack.append(item)
            total_value += item[0]
            total_weight += item[1]

    return knapsack, total_value, total_weight

def solve_without_x_element(items, capacity, knapsack, total_value, total_weight, x_th_element):
    #knapsack = sorted(knapsack, key=lambda x: x[1], reverse=True)
    unique_items = list(set(items) - set(knapsack))

    #print("Greedy:", knapsack)

    x_th_element_data = knapsack[x_th_element] #get data from x element
    del knapsack[x_th_element] #remove x element

    #print("W/out",x_th_element+1,":", knapsack)

    total_value -= x_th_element_data[0]
    total_weight -= x_th_element_data[1]

    #print(f'value {x_th_element_data[0]} , {x_th_element_data[1]}')

    for item in unique_items:
        if total_weight + item[1] <= capacity:
            knapsack.append(item)
            total_value += item[0]
            total_weight += item[1]

    return knapsack, total_value, total_weight

def solve_knapsack(items, capacity, x_th_element):
    knapsack, total_value, total_weight = solve_greedy_knapsack(items, capacity)
    if len(knapsack) == 0:
        return [], 0, 0

    #print(knapsack)

    knapsack_dantzig=knapsack[:]
    optimized_knapsack, optimized_total_value, optimized_total_weight = solve_without_x_element(items, capacity, knapsack, total_value, total_weight, x_th_element)

    #print(optimized_knapsack)

    if optimized_total_value > total_value:
        return optimized_knapsack, optimized_total_value, optimized_total_weight
    else:
        return knapsack_dantzig, total_value, total_weight
    

# Test
if __name__ == '__main__':
    items = [(1, 2), (2, 2), (3, 3), (3, 2), (5, 6), (4, 5), (6, 5)]
    capacity = 10
    x_th_element = 2

    print("Without", x_th_element, "th element: ", solve_knapsack(items, capacity, x_th_element)) # Expected: ([(1, 2), (2, 3), (4, 5), (5, 6)], 12, 16)
    print(solve_knapsack(items, capacity, 0)) # Expected: ([(2, 3), (3, 4), (4, 5), (5, 6)], 14, 17)

    print(len(items))

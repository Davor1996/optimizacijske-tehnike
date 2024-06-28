"""
    Solution to the 0/1 Knapsack problem using Dantzing's greedy algorithm.
"""

def solve_knapsack(items, capacity):
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

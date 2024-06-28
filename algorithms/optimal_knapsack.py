"""
    Basic solution with memoization for 0/1 Knapsack problem
    Medium article: https://medium.com/swlh/dynamic-programming-0-1-knapsack-python-code-222e607a2e8
"""

def solve_knapsack(items, capacity):
    n = len(items)
    if capacity <= 0 or n == 0:
        return 0
    
    dp = [[0 for x in range(capacity+1)] for y in range(n)]
    
    # Populate the capacity = 0 columns, with '0' capacity we have '0' profit
    for i in range(0, n):
        dp[i][0] = 0
    
    # If we have only one weight, we will take it if it is not more than the capacity
    for c in range(0, capacity+1):
        if items[0][1] <= c:
            dp[0][c] = items[0][0]
    
    for i in range(1, n):
        for c in range(1, capacity+1):
            profit1, profit2 = 0, 0
            if items[i][1] <= c:
                profit1 = items[i][0] + dp[i - 1][c - items[i][1]]

            profit2 = dp[i-1][c]
            dp[i][c] = max(profit1, profit2)
    
    # Maximum profit will be at the bottom-right corner.
    return dp[n-1][capacity]

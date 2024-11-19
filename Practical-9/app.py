import streamlit as st
class Item:
    def __init__(self, profit, weight):
        self.profit = profit
        self.weight = weight

def fractional_knapsack(W, profits, weights):
    items = [Item(profits[i], weights[i]) for i in range(len(profits))]
    items.sort(key=lambda x: x.profit / x.weight, reverse=True)
    total_value = 0.0
    fractions = []
    for item in items:
        if item.weight <= W:
            total_value += item.profit
            W -= item.weight
            fractions.append(1) 
        else:
            fraction = W / item.weight
            total_value += item.profit * fraction
            fractions.append(fraction)  
            break 

    return total_value, items, fractions
st.title("Fractional Knapsack Problem")
W = st.number_input("Enter the maximum weight capacity (W):", min_value=1, value=60)
num_items = st.number_input("Enter the number of items:", min_value=1, value=4)
profits = []
weights = []
for i in range(num_items):
    profit = st.number_input(f"Enter profit for item {i + 1}:", min_value=0, value=100 * (i + 1))
    weight = st.number_input(f"Enter weight for item {i + 1}:", min_value=1, value=10 * (i + 1))
    profits.append(profit)
    weights.append(weight)
if st.button("Calculate Maximum Profit"):
    max_profit, sorted_items, fractions = fractional_knapsack(W, profits, weights)
    sorted_profits = [item.profit for item in sorted_items]
    sorted_weights = [item.weight for item in sorted_items]
    ratios = [item.profit / item.weight for item in sorted_items]
    st.write("### Sorted by Profit-to-Weight Ratio:")
    st.write(f"Profits: {sorted_profits}")
    st.write(f"Weights: {sorted_weights}")
    st.write(f"Ratios: {ratios}")
    st.write(f"Fractions taken: {fractions}")
    st.success(f"Total profit: {max_profit}")

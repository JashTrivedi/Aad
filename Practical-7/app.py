import streamlit as st
import pandas as pd

# Knapsack function to solve the 0/1 knapsack problem
def knapsack(w, v, W):
    n = len(v)
    # Initialize a 2D list (table) to store maximum values
    table = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
      
    # Build the table in a bottom-up manner
    for i in range(1, n + 1):  # Loop through items
        for j in range(W + 1):  # Loop through each capacity
            if w[i - 1] <= j:
                # Take the maximum of including or not including the current item
                table[i][j] = max(table[i - 1][j], v[i - 1] + table[i - 1][j - w[i - 1]])
            else:
                # If the current item can't be included, skip it
                table[i][j] = table[i - 1][j]
    
    return table

# Streamlit app title
st.title("0/1 Knapsack Problem Solver")

# Input section
weights_input = st.text_input('Enter the weights of the items (comma-separated)', '2, 3, 4, 5')
values_input = st.text_input('Enter the values of the items (comma-separated)', '3, 4, 5, 6')
capacity = st.number_input('Enter the capacity of the knapsack', min_value=1, value=5)

# Solve the knapsack problem when button is clicked
if st.button("Solve Knapsack"):
    # Convert input strings to lists of integers
    weights = list(map(int, weights_input.split(',')))
    values = list(map(int, values_input.split(',')))

    # Calculate the table using the knapsack function
    table = knapsack(weights, values, capacity)
    
    # Find the maximum value in the knapsack
    max_value = table[len(weights)][capacity]

    # Display the maximum value
    st.write(f"Maximum value in knapsack: {max_value}")

    # Convert the table to a Pandas DataFrame for display
    column_names = [f"Capacity {i}" for i in range(capacity + 1)]
    df = pd.DataFrame(table, columns=column_names)

    # Display the table as a DataFrame
    st.subheader("Dynamic Programming Table")
    st.dataframe(df)

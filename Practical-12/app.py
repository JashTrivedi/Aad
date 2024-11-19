import numpy as np
import pandas as pd
import streamlit as st
from itertools import permutations

def tsp(distance_matrix):
    n = len(distance_matrix)
    cities = list(range(1, n))  # Cities excluding the starting city (city 0)
    min_cost = np.inf
    min_path = []

    # Generate all permutations of the cities
    for perm in permutations(cities):
        current_cost = 0
        current_path = [0]  # Start from city 0

        # Calculate the cost for this permutation
        for i in range(len(perm)):
            current_cost += distance_matrix[current_path[-1]][perm[i]]
            current_path.append(perm[i])

        # Return to the starting city (city 0)
        current_cost += distance_matrix[current_path[-1]][0]

        # Update if a better (cheaper) path is found
        if current_cost < min_cost:
            min_cost = current_cost
            min_path = current_path + [0]  # Complete the round trip

    return min_path, min_cost

def main():
    st.title("Traveling Salesman Problem Solver")

    # Input for the distance matrix
    st.subheader("Enter the distance matrix:")

    # Number of cities
    num_cities = st.number_input("Number of cities:", min_value=2, max_value=10, value=5, step=1)

    # Create input fields for the distance matrix
    st.subheader("Enter the distance matrix:")
    distance_matrix = []

    for i in range(num_cities):
        row = st.text_input(
            f"Enter distances for city {i + 1} (comma-separated, use '∞' for infinity):",
            value=",".join(['0' if j == i else '∞' for j in range(num_cities)])  # Default sample values
        )

        # Parse the row into a list, interpreting '∞' as np.inf and finite values as integers
        try:
            distance_matrix.append([
                np.inf if x.strip() == '∞' else int(x.strip()) for x in row.split(',')
            ])
        except ValueError:
            st.error("Please enter valid integer values or '∞' for infinity, separated by commas.")
            return

    # Display the distance matrix as a table
    display_matrix = pd.DataFrame(distance_matrix,
                                   columns=[f"City {i + 1}" for i in range(num_cities)],
                                   index=[f"City {i + 1}" for i in range(num_cities)]
                                  ).replace(np.inf, '∞')
    st.subheader("Distance Matrix:")
    st.table(display_matrix)

    if st.button("Calculate Minimum Path"):
        # Calculate the minimum path and cost
        min_path, min_cost = tsp(distance_matrix)

        # Output detailed path in table form with integer distances
        path_details = {
            "From City": [min_path[i] + 1 for i in range(len(min_path) - 1)],
            "To City": [min_path[i + 1] + 1 for i in range(len(min_path) - 1)],
            "Distance": [int(distance_matrix[min_path[i]][min_path[i + 1]]) for i in range(len(min_path) - 1)]
        }
        path_df = pd.DataFrame(path_details)
        st.subheader("Detailed Path Information")
        st.table(path_df)

        # Display the results
        readable_path = " → ".join([str(i + 1) for i in min_path])  # City numbers only
        st.subheader("Results")
        st.write(f"Minimum Cost: {min_cost}")
        st.write(f"Path Taken: {readable_path}")

if __name__ == "__main__":
    main()

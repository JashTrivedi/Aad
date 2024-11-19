import streamlit as st
import heapq
import pandas as pd

# Dijkstra's Algorithm
def dijkstra(graph, start_node):
    num_nodes = len(graph)
    distances = {node: float('inf') for node in range(num_nodes)}
    distances[start_node] = 0
    predecessors = {node: None for node in range(num_nodes)}
    min_heap = [(0, start_node)]

    while min_heap:
        current_distance, current_node = heapq.heappop(min_heap)

        if current_distance > distances[current_node]:
            continue

        for neighbor in range(num_nodes):
            weight = graph[current_node][neighbor]
            if weight != float('inf'):
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(min_heap, (distance, neighbor))

    return distances, predecessors

# Streamlit Input
st.title("Shortest Path Calculator (Dijkstra's Algorithm)")

# Input total number of nodes
num_nodes = st.number_input("Enter total number of nodes:", min_value=2, max_value=20, value=5, step=1)

# Generate character labels for nodes (e.g., A, B, C, ...)
node_labels = [chr(65 + i) for i in range(num_nodes)]

# Input starting node
start_node_char = st.selectbox("Enter the starting node:", node_labels)
start_node = node_labels.index(start_node_char)

# Input adjacency matrix
st.write("Enter the adjacency matrix below (use '∞' for no connection):")
adj_matrix = []

for i in range(num_nodes):
    row = st.text_input(f"Row {node_labels[i]} (comma-separated):", value=",".join(["∞" if i != j else "0" for j in range(num_nodes)]))
    try:
        # Convert input into a list of floats, replacing '∞' with infinity
        adj_matrix.append([float(x) if x != '∞' else float('inf') for x in row.split(",")])
        if len(adj_matrix[i]) != num_nodes:
            st.error(f"Row {node_labels[i]} must contain {num_nodes} values.")
            st.stop()  # Stop further execution if the row is incorrect
    except ValueError:
        st.error(f"Invalid input in row {node_labels[i]}. Please use numbers or '∞' for no connection.")
        st.stop()  # Stop further execution if there's an invalid input

# Display the adjacency matrix as a table
st.write("Adjacency Matrix:")
formatted_matrix = [[("∞" if cell == float('inf') else int(cell)) for cell in row] for row in adj_matrix]
st.table(pd.DataFrame(formatted_matrix, index=node_labels, columns=node_labels))

# Calculate shortest paths when the button is pressed
if st.button("Calculate Shortest Path"):
    try:
        distances, predecessors = dijkstra(adj_matrix, start_node)
    except ValueError:
        st.error("Invalid adjacency matrix. Please check your input.")
        st.stop()  # Stop if there's an issue with the matrix

    # Display shortest paths
    st.write(f"Shortest Paths from Node {start_node_char}:")
    paths = []

    # Add path from the starting node to itself (distance is 0)
    paths.append((node_labels[start_node], node_labels[start_node], 0))  # Distance to itself is 0

    # For each node, construct the path from start node
    for node in range(num_nodes):
        if node != start_node and distances[node] != float('inf'):
            path = []
            current = node
            while current is not None:
                path.insert(0, node_labels[current])
                current = predecessors[current]
            paths.append((node_labels[start_node], node_labels[node], int(distances[node])))  # Convert cost to int

    # Display the paths in a table
    st.table(pd.DataFrame(paths, columns=["Source", "Destination", "Cost"]))

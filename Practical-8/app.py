import streamlit as st
import pandas as pd

# Function to compute the LCS length table and direction table
def compute_lcs(A, B):
    # Get lengths of sequences
    m, n = len(A), len(B)
    
    # Initialize the dp array and direction array
    c = [[0] * (n + 1) for _ in range(m + 1)]
    d = [[""] * (n + 1) for _ in range(m + 1)]
    
    # Fill the dp array and direction array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i - 1] == B[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                d[i][j] = "↖"  # Diagonal (match)
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                d[i][j] = "↑"  # Up (from A)
            else:
                c[i][j] = c[i][j - 1]
                d[i][j] = "←"  # Left (from B)
    
    return c, d

# Streamlit app title
st.title('LCS Computation with Full Table Display')

# Input section for sequences
A_input = st.text_input('Enter the first sequence (comma-separated)', '1, 2, 3, 1')
B_input = st.text_input('Enter the second sequence (comma-separated)', '1, 4, 2, 3, 1')

# Add a button to trigger LCS table generation
if st.button('Generate LCS Tables'):
    # Convert input strings to lists of integers
    if A_input and B_input:
        try:
            A = [int(x.strip()) for x in A_input.split(',')]
            B = [int(x.strip()) for x in B_input.split(',')]

            # Compute the LCS dp table and direction table
            c_table, d_table = compute_lcs(A, B)

            # Convert c_table and d_table to DataFrames for display
            c_df = pd.DataFrame(c_table, columns=[f"B{j}" for j in range(len(B) + 1)], index=[f"A{i}" for i in range(len(A) + 1)])
            d_df = pd.DataFrame(d_table, columns=[f"B{j}" for j in range(len(B) + 1)], index=[f"A{i}" for i in range(len(A) + 1)])

            # Display the LCS dp table
            st.subheader("LCS Length Table (c[i][j])")
            st.dataframe(c_df)

            # Display the direction/arrow table
            st.subheader("Direction Table (d[i][j])")
            st.dataframe(d_df)

        except ValueError:
            st.error('Please enter valid comma-separated integers for both sequences.')

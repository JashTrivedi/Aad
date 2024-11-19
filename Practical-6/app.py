from flask import Flask, render_template, request, Response
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def print_optimal_parens(s, i, j):
    if i == j:
        return f"A{i+1}"  # Adjust for 1-based indexing
    else:
        return f"({print_optimal_parens(s, i, s[i][j])} x {print_optimal_parens(s, s[i][j] + 1, j)})"

def matrix_chain_order(p):
    n = len(p) - 1  # Number of matrices
    m = np.zeros((n, n), dtype=float)
    s = np.zeros((n, n), dtype=int)

    # Set all entries in m to infinity for later comparison
    for i in range(n):
        for j in range(n):
            m[i][j] = float('inf')
    # No multiplications needed for a single matrix
    for i in range(n):
        m[i][i] = 0

    # l is the chain length
    for l in range(2, n+1):
        for i in range(n-l+1):
            j = i + l - 1
            for k in range(i, j):
                q = m[i][k] + m[k+1][j] + p[i] * p[k+1] * p[j+1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    parens = None
    dimensions = (5, 10, 3, 12, 5, 50, 6)

    if request.method == 'POST':
        m, s = matrix_chain_order(dimensions)
        result = m[0][len(dimensions) - 2]
        parens = print_optimal_parens(s, 0, len(dimensions) - 2)

    return render_template('index.html', result=result, parens=parens, dimensions=dimensions)

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    test_cases = [
        (2, 3, 6, 4, 5),
        (10, 30, 5, 60),
        (5, 10, 3, 12, 5, 50, 6),
        (40, 20, 30, 10, 30)
    ]
    analysis_results = []
    dimensions_list = []
    min_multiplications = []

    for case in test_cases:
        m, s = matrix_chain_order(case)
        analysis_results.append({
            'dimensions': case,
            'min_multiplications': m[0][len(case) - 2],
            'optimal_parenthesization': print_optimal_parens(s, 0, len(case) - 2)
        })
        dimensions_list.append(f"{len(case) - 1} matrices")
        min_multiplications.append(m[0][len(case) - 2])

    # Plot the analysis using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(dimensions_list, min_multiplications, color='skyblue')
    ax.set_xlabel('Number of Matrices')
    ax.set_ylabel('Minimum Multiplications')
    ax.set_title('Minimum Scalar Multiplications for Different Matrix Chains')

    # Convert plot to PNG image for rendering in HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', analysis_results=analysis_results, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)

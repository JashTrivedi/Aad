from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64
import sys

app = Flask(__name__)
sys.setrecursionlimit(5000)

# Function for recursion
def sumUsingRecursion(n, counter):
    counter[0] += 1
    if n == 0:
        return 0
    else:
        return n + sumUsingRecursion(n - 1, counter)

# Function to calculate sum using loop
def calculate_sum_using_loop(N):
    iterations = 0
    total_sum = 0
    for i in range(1, N + 1):
        total_sum += i
        iterations += 1
    return iterations

# Function to calculate sum using equation
def calculate_sum_using_equation(N):
    iterations = 1
    total_sum = (N * (N + 1)) // 2
    return iterations

# Function to calculate sum using recursion
def calculate_sum_using_recursion(N, iterations=0):
    if N == 0:
        return iterations
    iterations += 1
    return calculate_sum_using_recursion(N - 1, iterations)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve and parse user input
        user_input = request.form.get('array', '')
        try:
            lst = list(map(int, user_input.split(',')))
        except ValueError:
            return "Invalid input. Please enter a comma-separated list of numbers."

        count_for_loop = []
        count_for_equation = []
        count_for_recursion = []

        for i in lst:
            # Iteration Method
            loop = calculate_sum_using_loop(i)
            count_for_loop.append(loop)

            # Equation Method
            equation = calculate_sum_using_equation(i)
            count_for_equation.append(equation)

            # Recursion Method
            recursion = [0]
            sumUsingRecursion(i, recursion)
            count_for_recursion.append(recursion[0])

        # Plotting a single combined graph
        plt.figure()
        plt.plot(lst, count_for_loop, color='r', linestyle='-', label='Iteration')
        plt.plot(lst, count_for_equation, color='b', linestyle='-', label='Equation')
        plt.plot(lst, count_for_recursion, color='g', linestyle='-', label='Recursion')
        plt.xlabel('Number')
        plt.ylabel('Operation Count')
        plt.legend()
        plt.title('Performance Comparison of Sum Calculation Methods')
        plt.grid(True)

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template('index.html', plot_url=plot_url,
                               numbers=lst,
                               count_loops=count_for_loop,
                               count_equations=count_for_equation,
                               count_recursions=count_for_recursion,
                               zip=zip)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64
import time

app = Flask(__name__)

def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def fibonacci_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        months = int(request.form['months'])

        # Calculate results for both methods and measure time
        start_time = time.time()
        recursive_results = [fibonacci_recursive(n) for n in range(1, months + 1)]
        recursive_time = time.time() - start_time

        start_time = time.time()
        iterative_results = [fibonacci_iterative(n) for n in range(1, months + 1)]
        iterative_time = time.time() - start_time

        # Prepare data for plotting
        plt.figure()
        plt.plot(range(1, months + 1), recursive_results, label='Recursive Method')
        plt.plot(range(1, months + 1), iterative_results, label='Iterative Method')
        plt.xlabel('Month')
        plt.ylabel('Number of Rabbit Pairs')
        plt.title('Rabbit Population Growth')
        plt.legend()
        plt.grid(True)

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        # Zip the results
        combined_results = zip(range(1, months + 1), recursive_results, iterative_results)

        return render_template('index.html',
                               plot_url=plot_url,
                               combined_results=combined_results,
                               recursive_time=recursive_time,
                               iterative_time=iterative_time)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

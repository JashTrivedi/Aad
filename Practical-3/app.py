from flask import Flask, render_template, request
import time
import random
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Custom filter to zip lists
@app.template_filter('zip')
def zip_filter(*args):
    return zip(*args)

# Sorting algorithms
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def measure_sorting_time(sort_function, data):
    start_time = time.time()
    sort_function(data)
    end_time = time.time()
    return end_time - start_time

def generate_food_quantities(n):
    return [random.randint(1, 1000) for _ in range(n)]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sizes = [int(x) for x in request.form.get('sizes', '10,50,100,500,1000').split(',')]
        bubble_sort_times = []
        insertion_sort_times = []
        merge_sort_times = []

        for n in sizes:
            data = generate_food_quantities(n)
            bubble_time = measure_sorting_time(bubble_sort, data.copy())
            insertion_time = measure_sorting_time(insertion_sort, data.copy())
            merge_time = measure_sorting_time(merge_sort, data.copy())

            bubble_sort_times.append(bubble_time)
            insertion_sort_times.append(insertion_time)
            merge_sort_times.append(merge_time)

        # Plotting
        fig, ax = plt.subplots()
        ax.plot(sizes, bubble_sort_times, 'ro-', label='Bubble Sort')
        ax.plot(sizes, insertion_sort_times, 'go-', label='Insertion Sort')
        ax.plot(sizes, merge_sort_times, 'bo-', label='Merge Sort')
        ax.set_xlabel('Input Size (n)')
        ax.set_ylabel('Time (seconds)')
        ax.legend()
        ax.set_title('Comparison of Sorting Methods')
        ax.grid(True)

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_url = base64.b64encode(img.getvalue()).decode('utf8')

        return render_template('index.html', img_url=img_url, sizes=sizes, bubble_times=bubble_sort_times, 
                               insertion_times=insertion_sort_times, merge_sort_times=merge_sort_times)

    return render_template('index.html', img_url=None)

if __name__ == '__main__':
    app.run(debug=True)

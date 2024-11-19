from flask import Flask, render_template, request, redirect, url_for
import time
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__)

# Dummy data for employees
employees = [
    {'emp_id': '1', 'name': 'Alice', 'age': 30, 'salary': 70000, 'designation': 'Engineer', 'mobile': '123-456-7890'},
    {'emp_id': '2', 'name': 'Bob', 'age': 25, 'salary': 50000, 'designation': 'Designer', 'mobile': '234-567-8901'},
    # Add more employee records here
]

def linear_search(data, key, attribute):
    for employee in data:
        if str(employee.get(attribute)).lower() == key.lower():
            return employee
    return None

def binary_search(data, key, attribute):
    data = sorted(data, key=lambda x: x.get(attribute))
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if str(data[mid].get(attribute)).lower() == key.lower():
            return data[mid]
        elif str(data[mid].get(attribute)).lower() < key.lower():
            low = mid + 1
        else:
            high = mid - 1
    return None

def generate_plot(linear_times, binary_times, sizes):
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, linear_times, 'b-o', label='Linear Search')
    plt.plot(sizes, binary_times, 'r-o', label='Binary Search')
    plt.xlabel('Number of Elements')
    plt.ylabel('Time (seconds)')
    plt.title('Search Times Comparison')
    plt.legend()
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

def get_employee_details():
    highest_salary = max(employees, key=lambda e: e['salary'], default={})
    lowest_salary_employee = min(employees, key=lambda e: e['salary'], default={})
    youngest_employee = min(employees, key=lambda e: e['age'], default={})
    oldest_employee = max(employees, key=lambda e: e['age'], default={})

    highest_package = highest_salary.get('designation', 'N/A')

    return highest_salary, lowest_salary_employee, youngest_employee, oldest_employee, highest_package

@app.route('/', methods=['GET', 'POST'])
def index():
    linear_search_time = binary_search_time = None
    linear_result = binary_result = None
    plot_url = None

    # Initialize employee details
    highest_salary = lowest_salary_employee = youngest_employee = oldest_employee = highest_package = None

    if request.method == 'POST':
        num_employees = int(request.form.get('num_employees'))
        search_key = request.form.get('search_key')
        search_attribute = request.form.get('search_attribute')

        start_time = time.time()
        linear_result = linear_search(employees, search_key, search_attribute)
        linear_search_time = time.time() - start_time

        start_time = time.time()
        binary_result = binary_search(employees, search_key, search_attribute)
        binary_search_time = time.time() - start_time

        sizes = [10, 50, 100, 200]
        linear_times = []
        binary_times = []

        for size in sizes:
            data = employees[:size]
            start_time = time.time()
            linear_search(data, search_key, search_attribute)
            linear_times.append(time.time() - start_time)

            start_time = time.time()
            binary_search(data, search_key, search_attribute)
            binary_times.append(time.time() - start_time)

        plot_url = generate_plot(linear_times, binary_times, sizes)

        # Get employee details for the table
        highest_salary, lowest_salary_employee, youngest_employee, oldest_employee, highest_package = get_employee_details()

    return render_template('index.html', linear_search_time=linear_search_time,
                           binary_search_time=binary_search_time,
                           linear_result=linear_result,
                           binary_result=binary_result,
                           plot_url=plot_url,
                           highest_salary=highest_salary,
                           lowest_salary_employee=lowest_salary_employee,
                           youngest_employee=youngest_employee,
                           oldest_employee=oldest_employee,
                           highest_package=highest_package)

if __name__ == '__main__':
    app.run(debug=True)

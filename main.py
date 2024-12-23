# print('Hello world')
import numpy as np
import arrr
from pyscript import document
from pyodide.ffi.wrappers import add_event_listener

def linear_regression(data):
    n = len(data)

    sum_x = sum_y = sum_xy = sum_x2 = 0

    for point in data:
        sum_x += point['x']
        sum_y += point['y']
        sum_xy += point['x'] * point['y']
        sum_x2 += point['x'] ** 2
    
    # Slope (m) & intersep (b)
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    b = (sum_y - m * sum_x) / n
    rounded_b = round(b/100000) * 100000
    
    return {'slope': round(m, 2), 'intercept': rounded_b}

dataset = [
    {'x': 10904365.52, 'y': 56151256.43},
    {'x': 10582321.11, 'y': 54556176.6},
    {'x': 10507249.39, 'y': 54604491.15},
    {'x': 10359392.8, 'y': 54381754.8},
    {'x': 10237611.49, 'y': 53796402.44}
]

result = linear_regression(dataset)

def predict(x):
    return result['slope'] * x + result['intercept']

predict_dataset = [
    10000000,
    10200000,
    10400000,
    10600000,
    10800000,
    11000000,
    11200000,
    11400000,
]

regression_data = [round(predict(x), 2) for x in predict_dataset]

def create_forward_difference_table(data):
    n = len(data)
    table = [[0] * n for _ in range(n)]
    
    for i in range(n):
        table[i][0] = data[i]['y']
    
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = table[i + 1][j - 1] - table[i][j - 1]
    
    return table

def newton_gregory_forward_interpolation(data, x_target):
    n = len(data)
    h = data[1]['x'] - data[0]['x'] 
    u = (x_target - data[0]['x']) / h

    diff_table = create_forward_difference_table(data)

    result = diff_table[0][0]
    u_product = 1
    factorial = 1
    
    for i in range(1, n):
        u_product *= (u - (i - 1))
        factorial *= i
        result += (u_product * diff_table[0][i]) / factorial
    
    return result

# x_target = [11377934.44, 10677887.15, 10657274.96, 10411801.22, 10452672, 10213705.17, 10046457.29]
# x_target = 0
dataset = [
    {'x': 10200000, 'y': 53646270.84},
    {'x': 10600000, 'y': 54977497.15},
    {'x': 11000000, 'y': 56308723.46},
    {'x': 11400000, 'y': 57639949.76},
]

# nilai_interpolasi = [round(newton_gregory_forward_interpolation(dataset, x), 2) for x in x_target]

def calculate_production(event):
    # Mengambil nilai dari input
    area = document.getElementById("area").value
    if area:
        area = float(area)
        result = newton_gregory_forward_interpolation(dataset, area)
        # Menampilkan hasil produksi
        document.getElementById("output").innerText = f"{result:,.2f}"
    else:
        document.getElementById("output").innerText = "Masukkan nilai area!"

# Menambahkan event listener ke tombol
calculate_btn = document.getElementById("calculate-btn")

add_event_listener(calculate_btn, "click", calculate_production)
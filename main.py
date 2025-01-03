# print('Hello world')
import numpy as np
import arrr
from pyscript import document
from pyodide.ffi.wrappers import add_event_listener

def moving_average_combined(data1, data2, window_size):
    """
    Menghitung moving average dari dua dataset yang digabungkan.
    
    Parameters:
        data1 (list): Dataset pertama (misalnya, data luas areal).
        data2 (list): Dataset kedua (misalnya, data hasil produksi).
        window_size (int): Ukuran jendela untuk rata-rata.
    
    Returns:
        list: Array of dictionaries dengan average dari dataset gabungan.
    """
    if len(data1) != len(data2):
        raise ValueError("Data1 dan Data2 harus memiliki panjang yang sama")
    
    if window_size <= 0 or window_size > len(data1):
        raise ValueError("Ukuran window tidak valid")
    
    moving_averages = []

    for i in range(len(data1) - window_size + 1):
        avg_x = sum(data1[i:i + window_size]) / window_size
        avg_y = sum(data2[i:i + window_size]) / window_size
        moving_averages.append({'x': round(avg_x, 2), 'y': round(avg_y, 2)})

    return moving_averages

dataLuasAreal = [11377934.44, 10677887.15, 10657274.96, 10411801.22, 10452672, 10213705.17, 10046457.29]
dataHasilProduksi = [59200533.72, 54604033.34, 54649202.24, 54415294.22, 54748977, 53980993.19, 52659237.12]
window_size = 3

mvDataset = moving_average_combined(dataLuasAreal, dataHasilProduksi, window_size)

# Output hasil
print(mvDataset)

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

result = linear_regression(mvDataset)
print(result)
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
print(regression_data)
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
regresi_dataset = [
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
        result = newton_gregory_forward_interpolation(regresi_dataset, area)
        # Menampilkan hasil produksi
        document.getElementById("output").innerText = f"{result:,.2f}"
    else:
        document.getElementById("output").innerText = "Masukkan nilai area!"

# Menambahkan event listener ke tombol
calculate_btn = document.getElementById("calculate-btn")

add_event_listener(calculate_btn, "click", calculate_production)
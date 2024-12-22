import timeit
import matplotlib.pyplot as plt
from prettytable import PrettyTable

class Product:
    def __init__(self, id, name):
        self.id = id
        self.name = name

# Implementasi Linear Search secara iteratif
def linear_search(products, target):
    for product in products:
        if product.name == target:
            return product
    return None

# Implementasi Linear Search secara rekursif
def linear_search_recursive(products, target, index=0):
    if index >= len(products):
        return None
    if products[index].name == target:
        return products[index]
    return linear_search_recursive(products, target, index + 1)

# Implementasi Binary Search secara iteratif
def binary_search(products, target):
    low, high = 0, len(products) - 1

    while low <= high:
        mid = (low + high) // 2
        if products[mid].name == target:
            return products[mid]
        elif products[mid].name < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

# Implementasi Binary Search secara rekursif
def binary_search_recursive(products, target, low, high):
    if low > high:
        return None

    mid = (low + high) // 2
    if products[mid].name == target:
        return products[mid]
    elif products[mid].name < target:
        return binary_search_recursive(products, target, mid + 1, high)
    else:
        return binary_search_recursive(products, target, low, mid - 1)

# Fungsi untuk mengukur waktu eksekusi secara deterministik
def measure_time(func, *args):
    repetitions = 1000
    timer = timeit.Timer(lambda: func(*args))
    return timer.timeit(number=repetitions) / repetitions

# Studi kasus dengan daftar produk
products = [Product(i, f"Product{i}") for i in range(1, 1001)]
products.sort(key=lambda product: product.name)

# Tabel untuk menyimpan hasil
results_table = PrettyTable()
results_table.field_names = ["n", "Linear Recursive Time (s)", "Linear Iterative Time (s)", 
                             "Binary Recursive Time (s)", "Binary Iterative Time (s)"]

# Menambahkan loop untuk pengujian dan perbandingan
while True:
    try:
        n = int(input("Masukkan nilai n (atau ketik -1 untuk keluar): "))
        if n == -1:
            break
        if n > len(products):
            print(f"Nilai n terlalu besar! Maksimal adalah {len(products)}.")
            continue

        subset = products[:n]
        target = subset[-1].name  # Pilih produk terakhir sebagai target pencarian

        # Waktu eksekusi untuk setiap metode pencarian
        linear_recursive_time = measure_time(linear_search_recursive, subset, target)
        linear_iterative_time = measure_time(linear_search, subset, target)
        binary_recursive_time = measure_time(binary_search_recursive, subset, target, 0, len(subset) - 1)
        binary_iterative_time = measure_time(binary_search, subset, target)

        # Tambahkan hasil ke tabel
        results_table.add_row([n, linear_recursive_time, linear_iterative_time, 
                               binary_recursive_time, binary_iterative_time])

        # Cetak tabel hasil
        print(results_table)

        # Plot hasil untuk Linear Search vs Binary Search
        sizes = [row[0] for row in results_table._rows]
        linear_recursive_times = [row[1] for row in results_table._rows]
        linear_iterative_times = [row[2] for row in results_table._rows]
        binary_recursive_times = [row[3] for row in results_table._rows]
        binary_iterative_times = [row[4] for row in results_table._rows]

        # Membuat grafik perbandingan
        plt.figure(figsize=(12, 8))

        plt.plot(sizes, linear_recursive_times, marker='o', label='Linear Recursive')
        plt.plot(sizes, linear_iterative_times, marker='o', label='Linear Iterative')
        plt.plot(sizes, binary_recursive_times, marker='x', label='Binary Recursive')
        plt.plot(sizes, binary_iterative_times, marker='x', label='Binary Iterative')

        plt.title('Performance Comparison: Linear vs Binary Search (Recursive & Iterative)')
        plt.xlabel('Input Size (n)')
        plt.ylabel('Execution Time (seconds)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except ValueError:
        print("Masukkan angka yang valid.")

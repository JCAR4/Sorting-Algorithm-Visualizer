import tkinter as tk
from tkinter import ttk
import random
import time
import threading

# Color constants
COLOR_DEFAULT = "#A9CCE3"
COLOR_COMPARE = "#F7DC6F"
COLOR_SWAP = "#E74C3C"
COLOR_SORTED = "#58D68D"

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.resizable(False, False)
        self.array = []
        self.speed = 0.05
        self.size = 50
        self.algorithm = "QuickSort"
        self.is_sorting = False

        self.setup_ui()
        self.generate_array()

    def setup_ui(self):
        control_frame = tk.Frame(self.root, padx=10, pady=5)
        control_frame.pack(fill=tk.X)

        tk.Label(control_frame, text="Algorithm:").pack(side=tk.LEFT)
        self.alg_menu = ttk.Combobox(control_frame, values=["QuickSort", "MergeSort", "HeapSort", "BubbleSort"], state="readonly", width=10)
        self.alg_menu.current(0)
        self.alg_menu.pack(side=tk.LEFT, padx=5)
        self.alg_menu.bind("<<ComboboxSelected>>", self.set_algorithm)

        tk.Label(control_frame, text="Size:").pack(side=tk.LEFT)
        self.size_scale = tk.Scale(control_frame, from_=10, to=150, orient=tk.HORIZONTAL, length=150, command=self.set_size)
        self.size_scale.set(self.size)
        self.size_scale.pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Speed:").pack(side=tk.LEFT)
        self.speed_scale = tk.Scale(control_frame, from_=1, to=100, orient=tk.HORIZONTAL, length=150, command=self.set_speed)
        self.speed_scale.set(int(100 - self.speed * 100))
        self.speed_scale.pack(side=tk.LEFT, padx=5)

        self.start_btn = tk.Button(control_frame, text="Start", command=self.start_sort)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.shuffle_btn = tk.Button(control_frame, text="Shuffle", command=self.generate_array)
        self.shuffle_btn.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack(pady=10)

    def set_algorithm(self, event=None):
        self.algorithm = self.alg_menu.get()

    def set_size(self, val):
        self.size = int(val)
        self.generate_array()

    def set_speed(self, val):
        self.speed = max(0.001, (100 - int(val)) / 100)

    def generate_array(self):
        if self.is_sorting:
            return
        self.array = [random.randint(10, 390) for _ in range(self.size)]
        self.draw_array()

    def draw_array(self, color_positions=None):
        self.canvas.delete("all")
        c_width = 800
        c_height = 400
        bar_width = c_width / len(self.array)
        for i, val in enumerate(self.array):
            x0 = i * bar_width
            y0 = c_height - val
            x1 = (i + 1) * bar_width
            y1 = c_height
            color = COLOR_DEFAULT
            if color_positions:
                if i in color_positions.get("compare", []):
                    color = COLOR_COMPARE
                elif i in color_positions.get("swap", []):
                    color = COLOR_SWAP
                elif i in color_positions.get("sorted", []):
                    color = COLOR_SORTED
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        self.root.update_idletasks()

    def start_sort(self):
        if self.is_sorting:
            return
        self.is_sorting = True
        threading.Thread(target=self.run_sort, daemon=True).start()

    def run_sort(self):
        if self.algorithm == "QuickSort":
            self.quick_sort(0, len(self.array) - 1)
        elif self.algorithm == "MergeSort":
            self.merge_sort(0, len(self.array) - 1)
        elif self.algorithm == "HeapSort":
            self.heap_sort()
        elif self.algorithm == "BubbleSort":
            self.bubble_sort()
        self.draw_array({"sorted": range(len(self.array))})
        self.is_sorting = False

    # Sorting Algorithms with visualization
    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            self.draw_array({"compare": [j, high]})
            time.sleep(self.speed)
            if self.array[j] < pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
                self.draw_array({"swap": [i, j]})
                time.sleep(self.speed)
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        self.draw_array({"swap": [i + 1, high]})
        time.sleep(self.speed)
        return i + 1

    def merge_sort(self, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(left, mid)
            self.merge_sort(mid + 1, right)
            self.merge(left, mid, right)

    def merge(self, left, mid, right):
        left_part = self.array[left:mid + 1]
        right_part = self.array[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            self.draw_array({"compare": [k]})
            time.sleep(self.speed)
            if left_part[i] <= right_part[j]:
                self.array[k] = left_part[i]
                i += 1
            else:
                self.array[k] = right_part[j]
                j += 1
            self.draw_array({"swap": [k]})
            time.sleep(self.speed)
            k += 1
        while i < len(left_part):
            self.array[k] = left_part[i]
            self.draw_array({"swap": [k]})
            time.sleep(self.speed)
            i += 1
            k += 1
        while j < len(right_part):
            self.array[k] = right_part[j]
            self.draw_array({"swap": [k]})
            time.sleep(self.speed)
            j += 1
            k += 1

    def heap_sort(self):
        n = len(self.array)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i)
        for i in range(n - 1, 0, -1):
            self.array[i], self.array[0] = self.array[0], self.array[i]
            self.draw_array({"swap": [i, 0]})
            time.sleep(self.speed)
            self.heapify(i, 0)

    def heapify(self, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and self.array[l] > self.array[largest]:
            largest = l
        if r < n and self.array[r] > self.array[largest]:
            largest = r
        if largest != i:
            self.draw_array({"compare": [i, largest]})
            time.sleep(self.speed)
            self.array[i], self.array[largest] = self.array[largest], self.array[i]
            self.draw_array({"swap": [i, largest]})
            time.sleep(self.speed)
            self.heapify(n, largest)

    def bubble_sort(self):
        n = len(self.array)
        for i in range(n):
            for j in range(0, n - i - 1):
                self.draw_array({"compare": [j, j + 1]})
                time.sleep(self.speed)
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.draw_array({"swap": [j, j + 1]})
                    time.sleep(self.speed)

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
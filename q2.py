import tkinter as tk
from tkinter import ttk, messagebox
import random
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify

def middle_rectangles(x1, x2, N, func, x):
    # Розрахунок ширини кожного прямокутника
    delta_x = (x2 - x1) / N
    
    # Підготовка списків для графіку
    x_points = []
    y_points = []
    rectangles = []
    
    # Ініціалізація змінної для зберігання суми площ
    area = 0
    
    # Цикл по кожному розбиттю
    for i in range(N):
        # Знаходимо середину кожного прямокутника
        midpoint = x1 + (i + 0.5) * delta_x
        x_points.append(midpoint)
        
        # Обчислюємо значення функції в точці середини
        f_value = func.subs(x, midpoint)
        y_points.append(float(f_value))
        
        # Додаємо прямокутники для графіку
        rect = {
            'x': midpoint - delta_x/2,
            'y': 0,
            'width': delta_x,
            'height': float(f_value)
        }
        rectangles.append(rect)
        
        # Додаємо площу прямокутника до загальної площі
        area += f_value * delta_x
    
    return area, x_points, y_points, rectangles

def trapezoidal(x1, x2, N, func, x):
    # Розрахунок ширини кожного інтервалу
    delta_x = (x2 - x1) / N
    
    # Підготовка списків для графіку
    x_points = [x1]
    y_points = [float(func.subs(x, x1))]
    trapezoids = []
    
    # Обчислюємо значення функції в кінцевих точках
    area = (func.subs(x, x1) + func.subs(x, x2)) / 2
    
    # Додаємо значення функції в проміжних точках
    for i in range(1, N):
        xi = x1 + i * delta_x
        x_points.append(xi)
        f_value = func.subs(x, xi)
        y_points.append(float(f_value))
        
        # Додаємо трапеції для графіку
        prev_x = x1 + (i-1) * delta_x
        prev_y = float(func.subs(x, prev_x))
        curr_y = float(f_value)
        
        trapezoid = {
            'x1': prev_x,
            'x2': xi,
            'y1': prev_y,
            'y2': curr_y
        }
        trapezoids.append(trapezoid)
        area += f_value
    
    # Додаємо кінцеву точку
    x_points.append(x2)
    y_points.append(float(func.subs(x, x2)))
    
    # Множимо на ширину інтервалу для отримання кінцевого результату
    area *= delta_x
    
    return area, x_points, y_points, trapezoids

def monte_carlo(x1, x2, N, func, x):
    # Генеруємо випадкові точки в межах [x1, x2]
    total_area = 0
    max_y = 0
    
    # Підготовка списків для графіку
    x_points = []
    y_points = []
    inside_points = []
    outside_points = []
    
    # Знаходимо максимальне значення функції
    x_max = np.linspace(x1, x2, 100)
    func_np = lambdify(x, func, 'numpy')
    max_y = max(func_np(x_max))
    
    for _ in range(N):
        # Випадкова точка по осі x та y
        random_x = random.uniform(x1, x2)
        random_y = random.uniform(0, max_y)
        
        # Значення функції в точці random_x
        f_value = func.subs(x, random_x)
        
        # Перевірка чи точка під кривою функції
        if random_y <= float(f_value):
            inside_points.append((random_x, random_y))
            total_area += f_value
        else:
            outside_points.append((random_x, random_y))
    
    # Обчислюємо середнє значення і множимо на (x2 - x1)
    area = (x2 - x1) * (total_area / N)
    
    return area, inside_points, outside_points

class IntegrationCalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Калькулятор інтегрування")
        master.geometry("500x300")

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.Frame(self.master, padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(input_frame, text="Нижня межа (x1):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.x1_entry = ttk.Entry(input_frame, width=20)
        self.x1_entry.grid(row=0, column=1, pady=5)
        self.x1_entry.insert(0, "0")

        ttk.Label(input_frame, text="Верхня межа (x2):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.x2_entry = ttk.Entry(input_frame, width=20)
        self.x2_entry.grid(row=1, column=1, pady=5)
        self.x2_entry.insert(0, "1")

        ttk.Label(input_frame, text="Функція:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.func_entry = ttk.Entry(input_frame, width=20)
        self.func_entry.grid(row=2, column=1, pady=5)
        self.func_entry.insert(0, "x**2")

        ttk.Label(input_frame, text="Кількість сегментів:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.segments_entry = ttk.Entry(input_frame, width=20)
        self.segments_entry.grid(row=3, column=1, pady=5)
        self.segments_entry.insert(0, "10")

        ttk.Label(input_frame, text="Метод:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.method_var = tk.StringVar()
        self.method_dropdown = ttk.Combobox(
            input_frame, 
            textvariable=self.method_var, 
            values=[
                "Метод середніх прямокутників", 
                "Трапецієвидний метод", 
                "Метод Монте-Карло"
            ], 
            state="readonly", 
            width=20
        )
        self.method_dropdown.grid(row=4, column=1, pady=5)
        self.method_dropdown.set("Метод середніх прямокутників")

        self.calculate_button = ttk.Button(input_frame, text="Обчислити", command=self.calculate)
        self.calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.result_var = tk.StringVar()
        self.result_label = ttk.Label(input_frame, textvariable=self.result_var, wraplength=400)
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)

    def calculate(self):
        try:
            x1 = float(self.x1_entry.get())
            x2 = float(self.x2_entry.get())
            N = int(self.segments_entry.get())
            func_str = self.func_entry.get()
            method = self.method_dropdown.get()

            x = symbols('x')
            func = sympify(func_str)
            
            x_np = np.linspace(x1, x2, 100)
            func_np = lambdify(x, func, 'numpy')

            plt.figure(figsize=(10, 6))
            
            plt.plot(x_np, func_np(x_np), label='Функція', color='blue')

            if method == "Метод середніх прямокутників":
                result, x_points, y_points, rectangles = middle_rectangles(x1, x2, N, func, x)
                
                # Малювання прямокутників
                for rect in rectangles:
                    plt.gca().add_patch(plt.Rectangle(
                        (rect['x'], rect['y']), 
                        rect['width'], rect['height'], 
                        fill=False, 
                        edgecolor='red'
                    ))
                
                plt.scatter(x_points, y_points, color='red', label='Точки середніх прямокутників', zorder=5)

            elif method == "Трапецієвидний метод":
                result, x_points, y_points, trapezoids = trapezoidal(x1, x2, N, func, x)
                
                # Малювання трапецій
                for trap in trapezoids:
                    plt.fill_between(
                        [trap['x1'], trap['x2']], 
                        [trap['y1'], trap['y2']], 
                        alpha=0.2, 
                        color='green'
                    )
                
                plt.scatter(x_points, y_points, color='green', label='Точки трапецій', zorder=5)

            else:  # Метод Монте-Карло
                result, inside_points, outside_points = monte_carlo(x1, x2, N, func, x)
                
                # Розділення точок на зелені (всередині) та червоні (зовні)
                inside_x = [p[0] for p in inside_points]
                inside_y = [p[1] for p in inside_points]
                outside_x = [p[0] for p in outside_points]
                outside_y = [p[1] for p in outside_points]
                
                plt.scatter(inside_x, inside_y, color='green', label='Точки в межах функції', zorder=5, alpha=0.7)
                plt.scatter(outside_x, outside_y, color='red', label='Точки поза функцією', zorder=5, alpha=0.7)

            plt.title(f'Інтегрування методом: {method}')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.legend()
            plt.grid(True)

            self.result_var.set(f"Результат інтегрування: {result}")

            plt.show()

        except Exception as e:
            messagebox.showerror("Помилка", str(e))

def main():
    root = tk.Tk()
    app = IntegrationCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
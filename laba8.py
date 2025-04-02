"""Задание на л.р. №8 ООП 24
Требуется написать объектно-ориентированную программу с графическим интерфейсом в соответствии со своим вариантом.
В программе должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
Ввод данных из файла с контролем правильности ввода.
Базы данных использовать нельзя. При необходимости сохранять информацию в виде файлов, разделяя значения запятыми или пробелами.
Для GUI использовать библиотеку tkinter.
Вариант 22
Объекты – квадраты
Функции:	масштабирование (увеличение, уменьшение)
визуализация
раскраска
поворот вокруг центра

"""

import tkinter as tk
from tkinter import filedialog, messagebox

class Square:
    def __init__(self, side=100, color="red", rotation=0):
        self.side = side  # Длина стороны
        self.color = color  # Цвет заливки
        self.rotation = rotation  # Угол поворота в градусах

    def scale(self, factor):
        """Масштабирование квадрата (увеличение/уменьшение)"""
        self.side = max(10, self.side * factor)  # Минимальный размер 10

    def rotate(self, angle):
        """Поворот квадрата вокруг центра"""
        self.rotation = (self.rotation + angle) % 360

    def set_color(self, new_color):
        """Изменение цвета квадрата"""
        self.color = new_color

    def draw(self, canvas, x, y):
        """Визуализация квадрата на Canvas"""
        half_side = self.side / 2
        # Координаты вершин без поворота
        points = [
            x - half_side, y - half_side,
            x + half_side, y - half_side,
            x + half_side, y + half_side,
            x - half_side, y + half_side
        ]
        # Поворот точек вокруг центра (x, y)
        if self.rotation != 0:
            import math
            angle_rad = math.radians(self.rotation)
            rotated_points = []
            for i in range(0, len(points), 2):
                dx = points[i] - x
                dy = points[i+1] - y
                new_dx = dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
                new_dy = dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
                rotated_points.extend([x + new_dx, y + new_dy])
            points = rotated_points
        canvas.create_polygon(points, fill=self.color, outline="black")

class SquareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление квадратами")
        self.square = Square()  # Создаем квадрат по умолчанию
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack(pady=10)
        self.setup_ui()

    def setup_ui(self):
        """Настройка интерфейса"""
        controls = tk.Frame(self.root)
        controls.pack(pady=5)

        # Масштабирование
        tk.Button(controls, text="Увеличить (+10%)", command=lambda: self.scale_square(1.1)).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Уменьшить (-10%)", command=lambda: self.scale_square(0.9)).pack(side=tk.LEFT, padx=5)

        # Поворот
        tk.Button(controls, text="Повернуть +45°", command=lambda: self.rotate_square(45)).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Повернуть -45°", command=lambda: self.rotate_square(-45)).pack(side=tk.LEFT, padx=5)

        # Цвет
        colors = ["red", "green", "blue", "yellow"]
        for color in colors:
            tk.Button(controls, text=color, bg=color, command=lambda c=color: self.change_color(c)).pack(side=tk.LEFT, padx=2)

        # Загрузка/сохранение
        tk.Button(self.root, text="Загрузить из файла", command=self.load_from_file).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(self.root, text="Сохранить в файл", command=self.save_to_file).pack(side=tk.RIGHT, padx=10, pady=5)

        # Отрисовка начального квадрата
        self.draw_square()

    def draw_square(self):
        """Отрисовка квадрата на Canvas"""
        self.canvas.delete("all")
        self.square.draw(self.canvas, 200, 200)  # Центр Canvas (400x400)

    def scale_square(self, factor):
        """Масштабирование и перерисовка"""
        self.square.scale(factor)
        self.draw_square()

    def rotate_square(self, angle):
        """Поворот и перерисовка"""
        self.square.rotate(angle)
        self.draw_square()

    def change_color(self, color):
        """Изменение цвета"""
        self.square.set_color(color)
        self.draw_square()

    def load_from_file(self):
        """Загрузка параметров квадрата из файла"""
        try:
            filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if not filepath:
                return
            with open(filepath, 'r') as file:
                data = file.read().strip().split(',')
                if len(data) != 3:
                    raise ValueError("Неверный формат данных")
                side = float(data[0])
                color = data[1]
                rotation = float(data[2])
                self.square = Square(side, color, rotation)
                self.draw_square()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки: {e}")

    def save_to_file(self):
        """Сохранение параметров квадрата в файл"""
        try:
            filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if not filepath:
                return
            with open(filepath, 'w') as file:
                file.write(f"{self.square.side},{self.square.color},{self.square.rotation}")
                messagebox.showinfo("Успех", "Данные сохранены!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SquareApp(root)
    root.mainloop()
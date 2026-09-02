import math

class Figure:
    """Базовый класс для всех фигур с инкапсуляцией координат"""
    
    def __init__(self, x=0, y=0):
        self.__x = x  
        self.__y = y  
    
    def get_coords(self):
        """Публичный метод для получения координат"""
        return (self.__x, self.__y)
    
    def set_coords(self, x, y):
        """Публичный метод для изменения координат"""
        self.__x = x
        self.__y = y
        print(f"Координаты изменены на ({x}, {y})")


class Circle(Figure):
    """Класс круга, наследуется от Figure"""
    
    def __init__(self, x=0, y=0, radius=1):
        super().__init__(x, y) 
        self.radius = radius
    
    def calculate_area(self):
        """Вычисляет площадь круга: π * r²"""
        return math.pi * self.radius ** 2
    
    def __str__(self):
        return f"Круг (центр: {self.get_coords()}, радиус: {self.radius})"


class Square(Figure):
    """Класс квадрата, наследуется от Figure"""
    
    def __init__(self, x=0, y=0, side=1):
        super().__init__(x, y)
        self.side = side
    
    def calculate_area(self):
        """Вычисляет площадь квадрата: side²"""
        return self.side ** 2
    
    def __str__(self):
        return f"Квадрат (центр: {self.get_coords()}, сторона: {self.side})"

print("=" * 50)
print("МИНИ-ГРАФИЧЕСКИЙ РЕДАКТОР")
print("=" * 50)
print()

print("1. Создаём фигуры:")
shapes = [
    Circle(0, 0, 3),           
    Square(1, 2, 4),           
    Circle(3, 4, 2.5),        
    Square(5, 6, 3),           
    Circle(7, 8, 1.5),         
]

for i, shape in enumerate(shapes, 1):
    print(f"  {i}. {shape}")

print()

print("2. Демонстрация инкапсуляции:")
print(f"   Координаты первой фигуры: {shapes[0].get_coords()}")
print("   Пробуем изменить координаты через метод set_coords()...")
shapes[0].set_coords(10, 20)
print(f"   Новые координаты: {shapes[0].get_coords()}")
print()

print("3. Вычисление общей площади (ПОЛИМОРФИЗМ):")
print("-" * 50)

total_area = 0
for i, shape in enumerate(shapes, 1):
    area = shape.calculate_area() 
    total_area += area
    print(f"   Фигура {i}: площадь = {area:.2f}")

print("-" * 50)
print(f"   ОБЩАЯ ПЛОЩАДЬ ВСЕХ ФИГУР: {total_area:.2f}")
print("=" * 50)

print()
print("4. Демонстрация полиморфизма (единый интерфейс):")
print("   Мы не знаем типы фигур, но вызываем calculate_area()!")
print("   Типы фигур в списке:")
for shape in shapes:
    print(f"   - {type(shape).__name__}")
class Figure:
    """Базовый класс для всех геометрических фигур"""
    
    def __init__(self, coords=(0, 0), width=1, color="black"):
        self.coords = coords
        self.width = width
        self.color = color
    
    def draw(self):
        """Метод рисования фигуры (будет переопределён в дочерних классах)"""
        print("Рисуется фигура")

class Line(Figure):
    """Класс линии"""
    
    def __init__(self, coords=(0, 0), width=1, color="black", length=10):
        super().__init__(coords, width, color)
        self.length = length
    
    def draw(self):
        print("Рисуется линия...")

class Rect(Figure):
    """Класс прямоугольника"""
    
    def __init__(self, coords=(0, 0), width=1, color="black", height=5):
        super().__init__(coords, width, color)
        self.height = height
    
    def draw(self):
        print("Рисуется прямоугольник...")


class Ellipse(Figure):
    """Класс эллипса"""
    
    def __init__(self, coords=(0, 0), width=1, color="black", radius=3):
        super().__init__(coords, width, color)
        self.radius = radius
    
    def draw(self):
        print("Рисуется эллипс...")

class Triangle(Figure):
    """Новый класс треугольника"""
    
    def __init__(self, coords=(0, 0), width=1, color="black", side=8):
        super().__init__(coords, width, color)
        self.side = side 
    
    def draw(self):
        print("Рисуется треугольник...")

print("Создаём список фигур (с треугольником):")
figures = [
    Line((1, 2), 2, "red", 15),
    Rect((3, 4), 3, "blue", 7),
    Ellipse((5, 6), 4, "green", 5),
    Triangle((7, 8), 5, "yellow", 6), 
]

print(f"В списке {len(figures)} фигур")
print()

print("Рисуем все фигуры:")
for figure in figures:
    figure.draw()
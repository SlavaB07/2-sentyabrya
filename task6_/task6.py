class Figure:
    """Базовый класс для всех геометрических фигур"""
    
    def __init__(self, coords=(0, 0), width=1, color="black"):
        self.coords = coords    
        self.width = width      
        self.color = color      


class Line(Figure):
    """Класс линии, наследуется от Figure"""
    
    def __init__(self, coords=(0, 0), width=1, color="black", length=10):

        super().__init__(coords, width, color)
        self.length = length    


class Rect(Figure):
    """Класс прямоугольника, наследуется от Figure"""
    
    def __init__(self, coords=(0, 0), width=1, color="black", height=5):

        super().__init__(coords, width, color)
        self.height = height    


class Ellipse(Figure):
    """Класс эллипса, наследуется от Figure"""
    
    def __init__(self, coords=(0, 0), width=1, color="black", radius=3):

        super().__init__(coords, width, color)
        self.radius = radius    

print("Создаём объекты фигур:")
print()

line = Line((1, 2), 2, "red", 15)
rect = Rect((3, 4), 3, "blue", 7)
ellipse = Ellipse((5, 6), 4, "green", 5)

print("=== Линия (Line) ===")
print(f"Координаты: {line.coords}")
print(f"Ширина: {line.width}")
print(f"Цвет: {line.color}")
print(f"Длина: {line.length}")
print()

print("=== Прямоугольник (Rect) ===")
print(f"Координаты: {rect.coords}")
print(f"Ширина: {rect.width}")
print(f"Цвет: {rect.color}")
print(f"Высота: {rect.height}")
print()

print("=== Эллипс (Ellipse) ===")
print(f"Координаты: {ellipse.coords}")
print(f"Ширина: {ellipse.width}")
print(f"Цвет: {ellipse.color}")
print(f"Радиус: {ellipse.radius}")
class Figure:
    def __init__(self, coords=(0, 0), width=1, color="black"):
        self.coords = coords
        self.width = width
        self.color = color
    def draw(self):
        print("Рисуется фигура")
class Line(Figure):
    def __init__(self, coords=(0, 0), width=1, color="black", length=10):
        super().__init__(coords, width, color)
        self.length = length
    def draw(self):
        print("Рисуется линия...")
class Rect(Figure):
    def __init__(self, coords=(0, 0), width=1, color="black", height=5):
        super().__init__(coords, width, color)
        self.height = height
    def draw(self):
        print("Рисуется прямоугольник...")
class Ellipse(Figure):
    def __init__(self, coords=(0, 0), width=1, color="black", radius=3):
        super().__init__(coords, width, color)
        self.radius = radius
    def draw(self):
        print("Рисуется эллипс...")
class Triangle(Figure):
    def __init__(self, coords=(0, 0), width=1, color="black", side=8):
        super().__init__(coords, width, color)
        self.side = side
    def draw(self):
        print("Рисуется треугольник...")
figures = [
    Line((1, 2), 2, "red", 15),
    Rect((3, 4), 3, "blue", 7),
    Ellipse((5, 6), 4, "green", 5),]
print("Рисуем все фигуры:")
for figure in figures:
    figure.draw()
print("\nДобавляем треугольник:")
figures.append(Triangle((7, 8), 5, "yellow", 6))
for figure in figures:
    figure.draw()
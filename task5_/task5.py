class Figure:
    """Базовый класс для всех геометрических фигур"""
    
    def __init__(self, coords=(0, 0), width=1, color="black"):
        self.coords = coords    
        self.width = width      
        self.color = color      


print("Создаём базовую фигуру:")
figure = Figure()
print(f"Координаты: {figure.coords}")
print(f"Ширина: {figure.width}")
print(f"Цвет: {figure.color}")
print()

print("Создаём фигуру с другими параметрами:")
figure2 = Figure((10, 20), 5, "red")
print(f"Координаты: {figure2.coords}")
print(f"Ширина: {figure2.width}")
print(f"Цвет: {figure2.color}")
class Graph:
    def __init__(self, x=0, y=0, scale=1.0):
        self._x = x          
        self._y = y
        self._scale = scale  

    def move(self, dx, dy):
        """Перемещает график на dx и dy"""
        self._x += dx
        self._y += dy
        print(f"График перемещён на ({dx}, {dy})")

    def change_scale(self, factor):
        """Изменяет масштаб графика"""
        self._scale *= factor
        print(f"Масштаб изменён в {factor} раз")

    def get_state(self):
        """Возвращает текущее состояние графика"""
        return f"x={self._x}, y={self._y}, scale={self._scale:.2f}"

print("Создаём три графика:")
g1 = Graph(1, 2, 1.0)
g2 = Graph(3, 4, 2.0)
g3 = Graph(5, 6, 0.5)

print(f"g1: {g1.get_state()}")
print(f"g2: {g2.get_state()}")
print(f"g3: {g3.get_state()}")
print()

print("--- Перемещаем g1 на (10, 5) ---")
g1.move(10, 5)

print("--- Изменяем масштаб g2 в 0.5 раз ---")
g2.change_scale(0.5)

print("--- g3 оставляем без изменений ---")
print()

print("Итоговое состояние графиков:")
print(f"g1: {g1.get_state()}")
print(f"g2: {g2.get_state()}")
print(f"g3: {g3.get_state()}")
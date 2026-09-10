class Point:
    def __init__(self, x, y, color='black'):
        self.x = x
        self.y = y
        self.color = color
points = [
    Point(10, 20),            
    Point(12, 5, 'red'),      
    Point(7, 15, 'blue')]
for p in points:
    print(f"({p.x}, {p.y}) — {p.color}")
import random
class Line:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)

class Rect:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)

class Ellipse:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)

elements = []
classes = [Line, Rect, Ellipse]

for _ in range(217):
    cls = random.choice(classes)
    a = random.randint(0, 100)
    b = random.randint(0, 100)
    c = random.randint(0, 100)
    d = random.randint(0, 100)

    obj = cls(a, b, c, d)
    elements.append(obj)

for obj in elements:
    if isinstance(obj, Line):
        obj.sp = (0, 0)
        obj.ep = (0, 0)

if __name__ == "__main__":
    line_count = sum(1 for obj in elements if isinstance(obj, Line))
    rect_count = sum(1 for obj in elements if isinstance(obj, Rect))
    ellipse_count = sum(1 for obj in elements if isinstance(obj, Ellipse))
    
    print(f"Всего объектов: {len(elements)}")
    print(f"Line: {line_count}")
    print(f"Rect: {rect_count}")
    print(f"Ellipse: {ellipse_count}")

    for obj in elements[:5]:
        if isinstance(obj, Line):
            print(f"Line: sp={obj.sp}, ep={obj.ep}")
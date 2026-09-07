class Cart:
    def __init__(self):
        self.goods = []

    def add(self, gd):
        self.goods.append(gd)

    def remove(self, indx):
        if 0 <= indx < len(self.goods):
            del self.goods[indx]

    def get_list(self):
        return [f"{item.name}: {item.price}" for item in self.goods]

class Table:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class TV:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Notebook:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cup:
    def __init__(self, name, price):
        self.name = name
        self.price = price

cart = Cart()

cart.add(TV("Samsung QLED", 150000))
cart.add(TV("LG OLED", 120000))
cart.add(Table("Дубовый стол", 25000))
cart.add(Notebook("MacBook Pro", 200000))
cart.add(Notebook("Lenovo ThinkPad", 80000))
cart.add(Cup("Фарфоровая кружка", 1500))

for item in cart.get_list():
    print(item)

print("\nУдаляем товар с индексом 1 (LG OLED):")
cart.remove(1)
for item in cart.get_list():
    print(item)
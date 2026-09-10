class Goods:
    title = "Мороженое"
    weight = 150
    tp = "Еда"
    price = 100
setattr(Goods, 'price', 2048)
setattr(Goods, 'inflation', 100)
print(Goods.price)
print(Goods.inflation)
class Cat:
    def __init__(self, breed, name, age):
        self.breed = breed
        self.name = name
        self.age = age

cat1 = Cat("Британская", "Король", 3)
cat2 = Cat("Сиамская", "Борис", 2)
cat3 = Cat("Дворовая", "Пушок", 5)

print(f"Кот 1: порода {cat1.breed}, имя {cat1.name}, возраст {cat1.age} лет")
print(f"Кот 2: порода {cat2.breed}, имя {cat2.name}, возраст {cat2.age} лет")
print(f"Кот 3: порода {cat3.breed}, имя {cat3.name}, возраст {cat3.age} лет")
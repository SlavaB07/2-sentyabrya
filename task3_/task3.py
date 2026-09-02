class Car:
    def __init__(self):
        self._engine_temperature = 20  

    def start_engine(self):
        self._engine_temperature = 90
        print("Двигатель прогрет")

    def drive(self):
        if self._engine_temperature >= 90:
            print("Поехали!")
        else:
            print("Сначала прогрейте двигатель!")


my_car = Car()

print(f"Температура двигателя (прямой доступ): {my_car._engine_temperature}°C")

print("Пробуем ехать без прогрева:")
my_car.drive()

print()

print("Прогреваем двигатель:")
my_car.start_engine()

print("Пробуем ехать после прогрева:")
my_car.drive()
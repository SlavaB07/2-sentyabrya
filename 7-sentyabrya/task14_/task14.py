class Money:
    def __init__(self, money):
        self.money = money

if __name__ == "__main__":
    my_money = Money(100)
    your_money = Money(1000)
    
    print(f"my_money: {my_money.money}")
    print(f"your_money: {your_money.money}")
class Fruit:
    # Члены класса
    # 1. Поля
    def __init__(self, name, color, gustus):
        self.name: str = name
        self.color: str = color
        self.gustus: str = gustus
    
    # 2. Методы    
    def maturus(self):
        print(f'Фрукт "{self.name}" созрел')

    def __str__(self) -> str:
        return f'{self.name}: {self.color}, {self.gustus}'


def main():
    f1 = Fruit('Яблоко', 'Зеленый', 'Кислый')    
    f1.maturus()
    print(f1)
    
if __name__ == '__main__':
    main()

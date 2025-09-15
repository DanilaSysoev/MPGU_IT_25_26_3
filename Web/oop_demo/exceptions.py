def v():
    try:
        print('Некоторые действия')
        raise ValueError('Error')
        print('Никогда не будет распечатано')
    except ArithmeticError as e:
        print(e)
    print('Продолжаем работу')
    

def f():
    try:
        print('Начинаем f')
        v()
        print('Этого никогда не увидим')
    except ImportError as e:
        print(e)
    print('Завершение f')
    

f()

def caller(func, *args, **kwargs):
    return func(*args, **kwargs)


def arithmetic(char):
    if char == '+':
        return lambda x, y: x + y
    elif char == '-':
        return lambda x, y: x - y
    elif char == '*':
        return lambda x, y: x * y
    elif char == '/':
        return lambda x, y: x / y
    raise ArithmeticError("Unknown operation")


def add_value(value):
    def sum_plus_value(lst):
        return sum(lst) + value
    return sum_plus_value


data1 = [1, 2, 3]
data2 = { "sep": "-", "end": '*' }

print(data1)
print(*data1)
print(*data1, data2)
print(*data1, **data2)

caller(print, *data1, **data2)
print()
summ = arithmetic('+')
print(summ(1, 2))

summator = add_value(100)
print(summator([1, 2, 3]))

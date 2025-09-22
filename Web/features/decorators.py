from functools import wraps


def simple_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("decoration")
        return func(*args, **kwargs)
    return wrapper


def deco_wrapper(message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(message)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@simple_decorator
def my_func(a, b):
    print(my_func.__name__)
    return a + b


@deco_wrapper("hello")
def my_func_2(a, b):
    return a * b

res = my_func(1, 2)
print(res)

res = my_func_2(4, 5)
print(res)

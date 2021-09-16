import math


def func_pass():
    pass


def func_add_ten(x):
    return x + 10


test_glob = 10


def func_with_globals():
    return test_glob


def func_with_import(x):
    return math.sin(x)


def func_with_recursion(x):
    if x <= 0:
        return 1
    return func_with_recursion(x - 1) * x


def func_with_func():
    x = 10

    def func():
        y = 15
        return x + y

    func()


def func_with_closure():
    x = 10

    def f():
        return x + 10

    return f


def wrapper_func(func):
    x = 10

    def wrapped(*args):
        func(*args)
        nonlocal x
        x += 1
        return x

    return wrapped


@wrapper_func
def check_decorator():
    pass

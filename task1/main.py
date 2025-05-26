

def strict(func):
    def inner(*args, **kwargs):
        args_array = list(args)
        args_prototype = list(func.__annotations__.values())[:-1]
        for index, value in enumerate(args_prototype):
            try:
                if not isinstance(args_array[index], value):
                    raise TypeError
            except IndexError:
                raise TypeError

        return func(*args, **kwargs)

    return inner


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError

def log_to_file(func):
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('notes.txt', 'a+') as f:
            f.write(f'your result for {func.__name__} is {result}\n')
        return result
    return wrap

@log_to_file
def add_thensq(a,b):
    result = a**2 + b
    return result

@log_to_file
def sub(a,b):
    return a-b

@log_to_file
def mult(a, b):
    return a*b


add_thensq(1,2)
sub(5,6)
mult(9,8.2)

# res = outer(add)
# print(res(1999999111103,42))
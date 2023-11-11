def outer(func):
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('notes.txt', 'w+') as f:
            f.write(f'you result is {result}')
        return result
    return wrap

def add(a,b):
    result = a**2 + b
    return result

def sub(a,b):
    return a-b

def mult(a, b):
    return a*b

# res = outer(add)
# print(res(1999999111103,42))
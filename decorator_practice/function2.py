def outer(y):
    x = 5
    def inner():
        y+=x
        return y
    return inner

# print(x)
result = outer(23)
print(result())
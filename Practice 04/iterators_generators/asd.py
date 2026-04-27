# x**2
def s(x):
    n = 0
    while n < x:
        yield n ** 2
        n += 1


for i in s(4):
    print(i)

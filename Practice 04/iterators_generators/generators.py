def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()
print(next(gen))
print(next(gen))
print(next(gen))

def countdown(num):
    print("Starting")
    while num > 0:
        yield num
        num -= 1

for val in countdown(5):
    print(val)

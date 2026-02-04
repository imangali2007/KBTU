numbers = [1, 2, 3, 4, 5]
squares_gen = (x*x for x in numbers)

print(next(squares_gen))
print(next(squares_gen))

for n in squares_gen:
    print(n)

print(sum(x*x for x in range(10)))

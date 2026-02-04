from functools import reduce

nums = [1, 2, 3, 4, 5]

sq = list(map(lambda x: x*x, nums))
print(sq)

evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)

total = reduce(lambda a, b: a + b, nums)
print(total)

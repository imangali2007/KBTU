prices = [100, 200, 300, 400]
discounted = list(map(lambda p: p * 0.9, prices))
print(discounted)

names = ["john", "jane", "doe"]
capitalized = list(map(lambda n: n.upper(), names))
print(capitalized)

power_levels = [10, 20, 30]
super_saiyan = list(map(lambda x: x * 50, power_levels))
print(super_saiyan)

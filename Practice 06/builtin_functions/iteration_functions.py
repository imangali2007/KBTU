for i in range(5):
    print(i)

fruits = ["apple", "banana", "cherry"]
for index, val in enumerate(fruits):
    print(f"{index}: {val}")

names = ["Alice", "Bob"]
ages = [25, 30]
for name, age in zip(names, ages):
    print(f"{name} is {age}")

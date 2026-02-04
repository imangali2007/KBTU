import random

print(random.randint(1, 10))

print(random.random())

mylist = ["apple", "banana", "cherry"]
print(random.choice(mylist))

random.shuffle(mylist)
print(mylist)

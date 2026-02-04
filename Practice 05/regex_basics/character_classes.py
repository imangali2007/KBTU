import re

txt = "The rain in Spain"

x = re.findall("[a-m]", txt)
print(x)

y = re.findall("[0-9]", "Order 25 and 100")
print(y)

z = re.findall("[^a-n]", txt)
print(z)

a = re.findall("[0123]", "Order 15, 20, 30")
print(a)

import re

txt = "The rain in Spain"

x = re.findall("\AThe", txt)
print(x)

y = re.findall(r"\bain", txt)
print(y)

z = re.findall("\d", "There are 25 apples")
print(z)

a = re.findall("\s", txt)
print(a)

b = re.findall("\w", txt)
print(b)

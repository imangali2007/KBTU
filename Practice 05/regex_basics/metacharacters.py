import re

txt = "The rain in Spain"

x = re.findall("^The.*Spain$", txt)
print(x)

y = re.findall("he..o", "hello world")
print(y)

z = re.findall("falls|stays", "The rain stays mainly in the plain")
print(z)

a = re.findall("a+", "The rain in Spain")
print(a)

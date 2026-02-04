import re

txt = "The rain in Spain"

x = re.search("Spain", txt)
print(x.start())

y = re.split("\s", txt)
print(y)

z = re.sub("\s", "9", txt)
print(z)

a = re.findall("Portugal", txt)
print(a)

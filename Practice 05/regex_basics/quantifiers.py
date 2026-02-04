import re

txt = "hello planet"

x = re.findall("he.{2}o", txt)
print(x)

y = re.findall("he.{2,}o", "heeeello world")
print(y)

z = re.findall("e{2}", "feel the eel")
print(z)

a = re.findall("e{1,3}", "feed the feeeed")
print(a)

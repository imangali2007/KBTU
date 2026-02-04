import re

txt = "The rain in Spain"

x = re.search("rain", txt, re.IGNORECASE)
print(x)

y = re.findall("spain", txt, re.IGNORECASE)
print(y)

z = re.search("^The", txt, re.MULTILINE)
print(z)

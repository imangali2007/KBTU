import re

txt = "The rain in Spain"

x = re.findall("ai", txt)
print(x)

y = re.findall("Portugal", txt)
print(y)

if not y:
  print("No match")

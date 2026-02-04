import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")

y = re.search(r"\bS\w+", txt)
print(y.group())
print(y.span())
print(y.string)

import json

x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

y = json.dumps(x)

print(y)

print(json.dumps(x, indent=4, separators=(". ", " = ")))

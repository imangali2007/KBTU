x = 300

def myfunc():
  print(x)

myfunc()
print(x)

def change_global():
    global x
    x = 200

change_global()
print(x)

x = "Global"

def outer():
    x = "Enclosing"
    def inner():
        x = "Local"
        print(x) 
    inner()
    print(x)

outer() 
print(x)

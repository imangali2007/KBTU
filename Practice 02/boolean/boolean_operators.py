a = 200
b = 33
c = 500

if a > b and c > a:
    print(True)

if a > b or a > c:
    print(True)

is_sunny = True
print(not is_sunny)

age = 25
has_license = True
has_car = False

can_drive_own_car = age >= 18 and has_license and has_car
print(can_drive_own_car)

can_rent_car = age > 21 and has_license
print(can_rent_car)

x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y)

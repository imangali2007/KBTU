class Spaceship:
    name = "Discovery"
    fuel = 100

    def fly(self):
        print("Whoosh! We are flying.")

ship = Spaceship()
print(ship.name)
print(ship.fuel)
ship.fly()

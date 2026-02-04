class Robot:
    population = 0

    def __init__(self, name):
        self.name = name
        Robot.population += 1

    def destroy(self):
        Robot.population -= 1
        print(f"{self.name} has been destroyed.")

r1 = Robot("R2-D2")
r2 = Robot("C-3PO")
print(Robot.population)

r3 = Robot("BB-8")
print(Robot.population)

r2.destroy()
print(Robot.population)

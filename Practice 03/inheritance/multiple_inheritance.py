class Flyer:
    def fly(self):
        print("Flying high!")

class Swimmer:
    def swim(self):
        print("Swimming deep!")

class Duck(Flyer, Swimmer):
    def quack(self):
        print("Quack!")

donald = Duck()
donald.fly()
donald.swim()
donald.quack()

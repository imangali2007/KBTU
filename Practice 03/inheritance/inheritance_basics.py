class Animal:
    def speak(self):
        print("Some sound")

class Dog(Animal):
    def bark(self):
        print("Woof!")

class Cat(Animal):
    def meow(self):
        print("Meow!")

d = Dog()
d.speak()
d.bark()

c = Cat()
c.speak()
c.meow()

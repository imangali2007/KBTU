class Player:
    def __init__(self, nickname, score):
        self.nickname = nickname
        self.score = score

p1 = Player("Destroyer99", 5000)
p2 = Player("Healer01", 3000)

print(p1.nickname)
print(p1.score)

print(p2.nickname)
print(p2.score)

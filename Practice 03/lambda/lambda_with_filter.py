scores = [65, 90, 45, 80, 55, 100]
passing = list(filter(lambda s: s >= 60, scores))
print(passing)

users = ["admin", "guest", "root", "user1", "anonymous"]
auth_users = list(filter(lambda u: len(u) > 4, users))
print(auth_users)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)

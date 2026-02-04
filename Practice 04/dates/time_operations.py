import datetime

now = datetime.datetime.now()
future = now + datetime.timedelta(days=10)
print(future)

past = now - datetime.timedelta(weeks=2)
print(past)

diff = future - past
print(diff.days)

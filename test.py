n = int(input())

nn = {i:a for i, a in zip(input().split(), input().split())}
c = input()
print(nn.get(c, 'Not found'))

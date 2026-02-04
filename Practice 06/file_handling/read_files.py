f = open("sample_files/example.txt", "r")
print(f.read())
f.close()

f = open("sample_files/example.txt", "r")
print(f.read(5))
f.close()

f = open("sample_files/example.txt", "r")
print(f.readline())
f.close()

f = open("sample_files/example.txt", "r")
for x in f:
  print(x)
f.close()

# 'r' - Read
# 'a' - Append
# 'w' - Write
# 'x' - Create
# 't' - Text
# 'b' - Binary

f = open("sample_files/example.txt", "rt")
print(f.read())
f.close()

f = open("sample_files/data.csv", "rb")
print(f.read())
f.close()

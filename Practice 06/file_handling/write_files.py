f = open("sample_files/example.txt", "a")
f.write("Now the file has more content!")
f.close()

f = open("sample_files/example.txt", "r")
print(f.read())
f.close()

f = open("sample_files/example.txt", "w")
f.write("Woops! I have deleted the content!")
f.close()

f = open("sample_files/example.txt", "r")
print(f.read())
f.close()

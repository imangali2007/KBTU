try:
    f = open("sample_files/myfile.txt", "x")
    f.write("New file created!")
    f.close()
except FileExistsError:
    print("File already exists")

f = open("sample_files/myfile.txt", "w")
f.write("Content overwritten")
f.close()

f = open("sample_files/myfile.txt", "r")
print(f.read())
f.close()

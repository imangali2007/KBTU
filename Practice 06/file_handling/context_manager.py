with open("sample_files/example.txt", "r") as f:
    data = f.read()
    print(data)

with open("sample_files/new_file.txt", "w") as f:
    f.write("Managed by context manager")

with open("sample_files/new_file.txt", "r") as f:
    print(f.read())

import os
import shutil
import string

def list_contents(path):
    print("Dirs:", [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
    print("Files:", [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])

def check_access(path):
    print(f"Exists: {os.access(path, os.F_OK)}")
    print(f"Readable: {os.access(path, os.R_OK)}")
    print(f"Writable: {os.access(path, os.W_OK)}")
    print(f"Executable: {os.access(path, os.X_OK)}")

def path_info(path):
    if os.path.exists(path):
        print("Filename:", os.path.basename(path))
        print("Directory:", os.path.dirname(path))

def count_lines(filename):
    with open(filename, 'r') as f:
        return len(f.readlines())

def write_list(filename, data):
    with open(filename, 'w') as f:
        for item in data:
            f.write(f"{item}\n")

def generate_files():
    if not os.path.exists("alpha"): os.mkdir("alpha")
    for char in string.ascii_uppercase:
        with open(f"alpha/{char}.txt", "w") as f:
            f.write(char)

def copy_file(src, dest):
    shutil.copy(src, dest)

def safe_delete(path):
    if os.path.exists(path) and os.access(path, os.W_OK):
        os.remove(path)

list_contents(".")
check_access("sample_files/example.txt")
path_info("sample_files/example.txt")
# generate_files()

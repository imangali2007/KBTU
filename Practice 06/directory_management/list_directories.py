import os

path = "."
files = os.listdir(path)
print(f"Files and dirs in {path}: {files}")

for root, dirs, files in os.walk(path):
    print(f"Root: {root}")
    print(f"Dirs: {dirs}")
    print(f"Files: {files}")
    break 

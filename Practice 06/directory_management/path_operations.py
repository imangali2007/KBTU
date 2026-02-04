import os

path = "sample_files/example.txt"

print(f"Exists: {os.path.exists(path)}")
print(f"Is file: {os.path.isfile(path)}")
print(f"Is dir: {os.path.isdir(path)}")
print(f"Base name: {os.path.basename(path)}")
print(f"Dir name: {os.path.dirname(path)}")
print(f"Split: {os.path.split(path)}")
print(f"Join: {os.path.join('folder', 'subfolder', 'file.txt')}")

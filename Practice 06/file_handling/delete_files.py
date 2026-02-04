import os

if os.path.exists("sample_files/myfile.txt"):
  os.remove("sample_files/myfile.txt")
  print("File deleted")
else:
  print("The file does not exist")

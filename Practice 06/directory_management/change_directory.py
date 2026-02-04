import os

print(f"Current: {os.getcwd()}")

os.chdir("..")
print(f"After change: {os.getcwd()}")

os.chdir("Practice 06")
print(f"Back to: {os.getcwd()}")

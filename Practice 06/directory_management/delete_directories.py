import os
import shutil

if os.path.exists("test_dir"):
    os.rmdir("test_dir")
    print("test_dir removed")

if os.path.exists("nested"):
    shutil.rmtree("nested")
    print("nested tree removed")

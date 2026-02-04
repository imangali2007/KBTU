import os

if not os.path.exists("test_dir"):
    os.mkdir("test_dir")
    print("Directory created")

if not os.path.exists("nested/dir/structure"):
    os.makedirs("nested/dir/structure")
    print("Nested directories created")

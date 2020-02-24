import os
import glob

for (path, dir, files) in os.walk("."):
    dir_name = str.split(path, "\\")[-1]
    if dir_name == "migrations":
        files = glob.glob(os.path.join(path, "*.py"))
        for file_path in files:
            if "__init__" not in file_path:
                print(file_path)
                os.remove(file_path)

    if dir_name == "__pycache__":
        files = glob.glob(os.path.join(path, "*.pyc"))

        for file_path in files:
            print(file_path)
            os.remove(file_path)

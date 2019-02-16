import os

def remove_file(path):
    os.remove(path)
    print(f'[info] image removed. path=[{path}]')

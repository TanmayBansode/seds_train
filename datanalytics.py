from glob import glob
from itertools import chain
from collections import Counter
from pprint import pprint
from model_data import id2class_map
import os

main_path = '.'  
print(main_path)

def get_folder_size_kb(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total_size += os.path.getsize(fp)
    return total_size // 1024  

def print_data_size(folder_type):
    data_size = len(glob(f'{main_path}/{folder_type}/labels/*.txt'))
    folder_size_kb = get_folder_size_kb(os.path.join(main_path, folder_type))
    print(f'{folder_type} data count: {data_size} | Total size: {folder_size_kb} KB')

def print_class_count(folder_type):
    class_list = []
    for file in glob(f'{main_path}/{folder_type}/labels/*.txt'):
        class_list.append([row.split()[0] for row in open(file, "r")])
    counter = Counter(list(chain(*class_list)))
    print(f'-- class-wise data count:')
    pprint({f'{k}. {id2class_map[k]}': v for k, v in counter.items()})
    print()


# Usage for your folders
for folder in ['violations']:
    print_data_size(folder)
    print_class_count(folder)

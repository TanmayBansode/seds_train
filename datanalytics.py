from glob import glob
from itertools import chain
from collections import Counter
from pprint import pprint

id2class_map = {
    '0': 'No Parking',
    '1': 'Not Wearing Helmet',
    '2': 'Triple Riding',
    '3': 'Usage Of Phone While Riding',
    '4': 'Wheeling',
    '5': 'Pothole'
}

main_path = '.' 
print(main_path)

def print_data_size(folder_type):
    data_size = len(glob(f'{main_path}/{folder_type}/labels/*.txt')) # all .txt files from labels folder of train or test folder
    print(f'{folder_type} data count: {data_size}')

def print_class_count(folder_type):
    class_list = []
    for file in glob(f'{main_path}/{folder_type}/labels/*.txt'): # for each file 
        class_list.append([row.split()[0] for row in open(file, "r")]) # for each line extract 1st element (label)
    counter = Counter(list(chain(*class_list)))
    print(f'-- data class count')
    pprint({f'{k}. {id2class_map[k]}':v for k, v in counter.items()}) # how many of each class with correct label from id2class map
    print()

print_data_size('train')
print_class_count('train')
print_data_size('valid')
print_class_count('valid')
print_data_size('test')
print_class_count('test')
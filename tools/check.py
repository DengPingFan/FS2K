import json
from collections import Counter
import math
import numpy as np


json_file_train = '../FS2K/anno_train.json'
json_file_test = '../FS2K/anno_test.json'


with open(json_file_train, 'r') as f:
    json_data = json.loads(f.read())

attrs = {}
for attr in json_data[0].keys():
    attrs[attr] = []
for idx_fs, fs in enumerate(json_data):
    for attr in fs:
        attrs[attr].append(fs[attr])

print('Total count of set:')
to_be_fixed = []
for attr, v in attrs.items():
    print('\t', attr, len(v))
    if 'hair_color' in attr or 'color' not in attr and 'name' not in attr:
        print('\t'*2, Counter(v))
    if 'color' in attr:
        to_be_fixed.append([])
        for idx_vv, vv in enumerate(v):
            vv = str(vv)
            if '[' in vv:
                if 'nan' in vv or vv == '[]':
                    to_be_fixed[-1].append(attrs['image_name'][idx_vv])
                    print('\t'*2, attrs['image_name'][idx_vv], attr, vv)
        if not to_be_fixed[-1]:
            to_be_fixed.pop()
# for idx_tbf, tbf in enumerate(to_be_fixed[:-1]):
#     print(to_be_fixed[idx_tbf] == to_be_fixed[idx_tbf+1])
# print(tbf)
print(json_data[0])

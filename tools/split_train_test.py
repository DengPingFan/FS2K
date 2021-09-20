import os
import json
import shutil


def add_suffix(file_path):
    if os.path.exists(file_path+'.jpg'):
        file_path += '.jpg'
    else:
        file_path += '.png'
    return file_path

json_files = {
    'train': '../FS2K/anno_train.json',
    'test': '../FS2K/anno_test.json'
}

os.makedirs('../FS2K/train/photo', exist_ok=True)
os.makedirs('../FS2K/train/sketch', exist_ok=True)
os.makedirs('../FS2K/test/photo', exist_ok=True)
os.makedirs('../FS2K/test/sketch', exist_ok=True)
for data_split, json_file in json_files.items():
    with open(json_file, 'r') as f:
        json_data = json.loads(f.read())

    attrs = {}
    for attr in json_data[0].keys():
        attrs[attr] = []
    for idx_fs, fs in enumerate(json_data):
        for attr in fs:
            attrs[attr].append(fs[attr])

    for image_name in attrs['image_name']:
        src = os.path.join('../FS2K/photo', image_name)
        dst = os.path.join('../FS2K', data_split, 'photo', image_name.replace('/image', '_image'))
        shutil.copy2(add_suffix(src), add_suffix(dst))
        src = src.replace('image', 'sketch').replace('photo', 'sketch')
        dst = dst.replace('image', 'sketch').replace('photo', 'sketch')
        shutil.copy2(add_suffix(src), add_suffix(dst))
        print(src, '-->', dst)

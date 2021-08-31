import os
import json
import numpy as np
import cv2
import matplotlib.pyplot as plt


root_dir = '../FS2K'
root_dir_photo = os.path.join(root_dir, 'photo')
root_dir_sketch = os.path.join(root_dir, 'sketch')

photo_paths = []
for photo_dir in os.listdir(root_dir_photo):
    photo_dir = os.path.join(root_dir_photo, photo_dir)
    photo_paths += sorted(os.listdir(photo_dir))


json_file_train = os.path.join(root_dir, 'anno_train.json')
json_file_test = os.path.join(root_dir, 'anno_test.json')


with open(json_file_test, 'r') as f:
    json_data = json.loads(f.read())

attrs = {}
for attr in json_data[0].keys():
    attrs[attr] = []
for idx_fs, fs in enumerate(json_data):
    for attr in fs:
        attrs[attr].append(fs[attr])

for idx_image_name, image_name in enumerate(attrs['image_name']):
    if idx_image_name < 0:
        continue
    print('{}/{},'.format(idx_image_name+1, len(attrs['image_name'])), image_name)
    image_name += '.jpg'
    # Attributes
    if 'nan' in attrs['lip_color'][idx_image_name]:
        skin_color = 'nan'
        lip_color = 'nan'
        eye_color = 'nan'
        hair_color = 'nan'
    else:
        skin_color = np.array(attrs['skin_color'][idx_image_name]).astype(int).tolist()
        lip_color = np.array(attrs['lip_color'][idx_image_name]).astype(np.uint8)
        eye_color = np.array(attrs['eye_color'][idx_image_name]).astype(np.uint8)
        hair_color = np.array(attrs['hair_color'][idx_image_name]).astype(np.uint8)
    hair = int(attrs['hair'][idx_image_name])
    gender = int(attrs['gender'][idx_image_name])
    earring = int(attrs['earring'][idx_image_name])
    smile = int(attrs['smile'][idx_image_name])
    frontal_face = int(attrs['frontal_face'][idx_image_name])
    style = int(attrs['style'][idx_image_name])

    # Processing
    photo_path = os.path.join(root_dir, 'photo', image_name)
    photo = cv2.imread(photo_path)
    sketch_path = os.path.join(root_dir, 'photo', image_name).replace('photo', 'sketch').replace('image', 'sketch')
    sketch = cv2.imread(sketch_path)
    if sketch is None:
        sketch = cv2.imread(sketch_path.replace('.jpg', '.png'))
        if sketch is None:
            sketch = cv2.imread(sketch_path.replace('.png', '.jpg'))
    split_line = np.zeros((photo.shape[0], 10, 3), dtype=photo.dtype)
    if 'nan' not in attrs['lip_color'][idx_image_name]:
        cv2.rectangle(photo, (skin_color[0] - 10, skin_color[1] - 10), (skin_color[0] + 10, skin_color[1] + 10), (0, 0, 255), 1)
    lip_color_region = (np.zeros((photo.shape[0], 50, 3)) + lip_color[::-1]).astype(photo.dtype)
    eye_color_region = (np.zeros((photo.shape[0], 50, 3)) + eye_color[::-1]).astype(photo.dtype)
    # for i in [photo, split_line, sketch, split_line, lip_color_region, split_line, eye_color_region]:
    #     print(i.shape)
    # comp = cv2.hconcat([photo, split_line, cv2.resize(sketch, photo.shape[:2][::-1], cv2.INTER_LINEAR), split_line, lip_color_region, split_line, eye_color_region])
    comp = cv2.hconcat([photo, split_line, sketch, split_line, lip_color_region, split_line, eye_color_region])
    plt.figure(figsize=(16, 10))
    plt.imshow(cv2.cvtColor(comp, cv2.COLOR_BGR2RGB))
    if hair == 0:
        hair = 'Yes'
    else:
        hair = 'No'
    if hair_color == 0:
        hair_color = 'Brown'
    elif hair_color == 1:
        hair_color = 'Black'
    elif hair_color == 2:
        hair_color = 'Red'
    elif hair_color == 3:
        hair_color = 'No'
    elif hair_color == 4:
        hair_color = 'Golden'
    if gender == 0:
        gender = 'Male'
    else:
        gender = 'Female'
    if earring == 0:
        earring = 'Yes'
    else:
        earring = 'No'
    if smile == 0:
        smile = 'No'
    else:
        smile = 'Yes'
    if frontal_face == 0:
        frontal_face = '<=30'
    else:
        frontal_face = '>30'
    style += 1
    plt.title('{}\nskin color selection region={},\nlip color={} (1st color bar),\neye color={}  (2nd color bar),\nhair={}, hair color={}, gender={}, earring={}, smile={}, frontal_face={}, style={}'.format(
        os.path.join('photo', image_name), skin_color, lip_color, eye_color, hair, hair_color, gender, earring, smile, frontal_face, style
    ))
    plt.show()




import os
import random
import shutil
from glob import glob

source_folder = './helmet'
train_folder = './h-train'
valid_folder = './h-valid'
train_split = 0.8  

for base in [train_folder, valid_folder]:
    os.makedirs(os.path.join(base, 'images'), exist_ok=True)
    os.makedirs(os.path.join(base, 'labels'), exist_ok=True)

image_paths = sorted(glob(os.path.join(source_folder, 'images', '*.png')))  # or *.png
random.shuffle(image_paths)

split_idx = int(len(image_paths) * train_split)
train_images = image_paths[:split_idx]
valid_images = image_paths[split_idx:]

def move_files(image_list, dest_folder):
    for img_path in image_list:
        filename = os.path.basename(img_path)
        label_path = os.path.join(source_folder, 'labels', filename.replace('.png', '.txt'))

        if not os.path.exists(label_path):
            print(f"[SKIP] No label for {filename}")
            continue

        shutil.copy2(img_path, os.path.join(dest_folder, 'images', filename))

        shutil.copy2(label_path, os.path.join(dest_folder, 'labels', filename.replace('.png', '.txt')))

        print(f"[✓] Moved {filename} to {dest_folder}")

print("\n[Splitting into TRAIN]")
move_files(train_images, train_folder)

print("\n[Splitting into VALID]")
move_files(valid_images, valid_folder)

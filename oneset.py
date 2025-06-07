import os
import shutil
from glob import glob

combined_path = './combined'
output_path = '.'  

split_types = ['train', 'valid']
image_exts = ['jpg', 'png']

for split in split_types:
    # Create output dirs
    img_dir = os.path.join(output_path, split, 'images')
    lbl_dir = os.path.join(output_path, split, 'labels')
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(lbl_dir, exist_ok=True)

    # Find matching images and labels
    for ext in image_exts:
        images = glob(os.path.join(combined_path, 'images', f'{split}_*.{ext}'))
        for img_path in images:
            base = os.path.splitext(os.path.basename(img_path))[0]
            label_path = os.path.join(combined_path, 'labels', base + '.txt')

            # New destination names (without prefix)
            new_name = '_'.join(base.split('_')[1:])  # remove 'train_' or 'valid_'
            new_img_path = os.path.join(img_dir, new_name + '.' + ext)
            new_lbl_path = os.path.join(lbl_dir, new_name + '.txt')

            shutil.copy(img_path, new_img_path)
            if os.path.exists(label_path):
                shutil.copy(label_path, new_lbl_path)

print("✅ Split complete: 'train' and 'valid' folders ready.")

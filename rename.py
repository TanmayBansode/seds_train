import os
from glob import glob
from shutil import move

main_path = './TripleSeat'  
folders = ['train', 'valid']

def rename_images_and_labels(folder):
    image_folder = os.path.join(main_path, folder, 'images')
    label_folder = os.path.join(main_path, folder, 'labels')

    image_paths = sorted(glob(os.path.join(image_folder, '*.jpg')))  # or .png if your images are in png
    for idx, image_path in enumerate(image_paths, start=1):
        new_name = f'tripleseat{idx}'
        ext = os.path.splitext(image_path)[1]
        
        old_image_name = os.path.basename(image_path)
        old_label_name = old_image_name.replace(ext, '.txt')
        old_label_path = os.path.join(label_folder, old_label_name)

        new_image_path = os.path.join(image_folder, new_name + ext)
        new_label_path = os.path.join(label_folder, new_name + '.txt')

        # Rename image
        move(image_path, new_image_path)
        print(f'Renamed image: {old_image_name} → {new_name + ext}')
        
        # Rename label file if it exists
        if os.path.exists(old_label_path):
            move(old_label_path, new_label_path)
            print(f'Renamed label: {old_label_name} → {new_name + ".txt"}')
        else:
            print(f'Label not found for: {old_image_name}, skipping label rename.')

# Run for both folders
for folder in folders:
    print(f'\nProcessing folder: {folder}')
    rename_images_and_labels(folder)

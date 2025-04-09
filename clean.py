import os
from glob import glob

main_path = './'
folders = ['train', 'valid']

classes_to_delete = {'0'}
rename_from = '6'
rename_to = '5'

def should_delete_file(label_lines):
    """Return True if all lines are in delete list."""
    class_ids = [line.strip().split()[0] for line in label_lines]
    return all(cls in classes_to_delete for cls in class_ids)

def should_rename_only(label_lines):
    """Return True if all lines are '6'."""
    class_ids = [line.strip().split()[0] for line in label_lines]
    return all(cls == rename_from for cls in class_ids)

def process_folder(folder_type):
    label_files = glob(f'{main_path}/{folder_type}/labels/*.txt')
    
    for label_path in label_files:
        with open(label_path, 'r') as f:
            lines = f.readlines()

        if not lines:
            continue  # skip empty files

        # Delete
        if should_delete_file(lines):
            print(f"[DELETE] {label_path}")
            os.remove(label_path)

            # Delete corresponding image
            image_name = os.path.basename(label_path).replace('.txt', '.jpg')
            image_path = os.path.join(main_path, folder_type, 'images', image_name)
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"         └─ Deleted image {image_path}")

        # Rename 'x' → 'y'
        if should_rename_only(lines):
            print(f"[RENAME] {label_path}")
            new_lines = [line.replace(f"{rename_from} ", f"{rename_to} ", 1) for line in lines]
            with open(label_path, 'w') as f:
                f.writelines(new_lines)

for folder in folders:
    print(f"\nProcessing {folder}...")
    process_folder(folder)

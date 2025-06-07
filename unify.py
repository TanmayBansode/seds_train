import os
import shutil

base_path = './violations'

datasets = ['helmet', 'TripleSeat', 'cell']  # add more if needed

# Root train and valid folders to create
sets = ['train', 'valid']
subfolders = ['images', 'labels']

# Create the unified folders if they don't exist
for set_type in sets:
    for subfolder in subfolders:
        os.makedirs(os.path.join(base_path, set_type, subfolder), exist_ok=True)

# Copy data from each dataset folder
for dataset in datasets:
    for set_type in sets:
        for subfolder in subfolders:
            src_folder = os.path.join(base_path, dataset, set_type, subfolder)
            dst_folder = os.path.join(base_path, set_type, subfolder)
            if not os.path.exists(src_folder):
                continue
            for filename in os.listdir(src_folder):
                src_file = os.path.join(src_folder, filename)
                dst_file = os.path.join(dst_folder, filename)
                if os.path.isfile(src_file):
                    # If a file with the same name exists, rename to avoid conflict
                    new_name = f"{dataset}_{filename}" if os.path.exists(dst_file) else filename
                    shutil.copy(src_file, os.path.join(dst_folder, new_name))
                    print(f"Copied {src_file} -> {os.path.join(dst_folder, new_name)}")

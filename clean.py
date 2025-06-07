import os
from glob import glob

main_path = './vehicle_big'
folders = ['train', 'valid']

#  truck + tempo, 0 & 3
#  cyclist 1
#  bike 2
#  car + jeep + taxi 4 & 5 & 13
#  toto + e-rickshaw + auto-rickshaw + cycle-rickshaw 6 & 7 & 8 & 11
#  bus + van 9 & 10
#  person 12

classes_to_delete = {}  

# Use a dictionary for multiple renaming rules
rename_map = {
    '0' : '11',
    '1' : '1',
    '2' : '2',
    '3' : '10',
    '4' : '5',
    '5' : '7',
    '6' : '4',
    '7' : '3',
    '8' : '4',
    '9' : '9',
    '10': '8',
    '11': '3',
    '12': '0',
    '13': '6',
}
def process_folder(folder_type):
    label_files = glob(f'{main_path}/{folder_type}/labels/*.txt')
    
    for label_path in label_files:
        with open(label_path, 'r') as f:
            lines = f.readlines()

        if not lines:
            continue  # skip empty files

        # Step 1: Remove lines with unwanted class ids
        new_lines = [line for line in lines if line.strip().split()[0] not in classes_to_delete]

        # Step 2: Delete file and image if no valid lines left
        if not new_lines:
            print(f"[DELETE] All lines removed in {label_path}, deleting file and image.")
            os.remove(label_path)

            image_name = os.path.basename(label_path).replace('.txt', '.jpg')
            image_path = os.path.join(main_path, folder_type, 'images', image_name)
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"         └─ Deleted image {image_path}")
            continue

        # Step 3: Apply renaming rules line-by-line
        updated_lines = []
        for line in new_lines:
            parts = line.strip().split()
            class_id = parts[0]
            if class_id in rename_map:
                parts[0] = rename_map[class_id]
                print(f"[RENAME] {class_id} → {parts[0]} in {label_path}")
            updated_lines.append(" ".join(parts) + "\n")

        # Step 4: Write updated lines back
        with open(label_path, 'w') as f:
            f.writelines(updated_lines)

for folder in folders:
    print(f"\nProcessing {folder}...")
    process_folder(folder)

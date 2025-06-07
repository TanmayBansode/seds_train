import os
from glob import glob

LABEL_TO_SEARCH = "3"
LABELS_FOLDER = "./vehicle_big/train/labels"

def search_label_in_files(label_folder, target_label):
    results = []

    txt_files = glob(os.path.join(label_folder, "*.txt"))

    for file_path in txt_files:
        with open(file_path, "r") as file:
            lines = file.readlines()

        matches = [line for line in lines if line.strip().startswith(f"{target_label} ")]
        if matches:
            results.append({
                "file": os.path.basename(file_path),
                "count": len(matches),
                "lines": matches
            })

    return results

label_occurrences = search_label_in_files(LABELS_FOLDER, LABEL_TO_SEARCH)

for result in label_occurrences:
    print(f"[{result['file']}] → {result['count']} occurrence(s) of label {LABEL_TO_SEARCH}")
    for line in result["lines"]:
        print("   └─", line.strip())

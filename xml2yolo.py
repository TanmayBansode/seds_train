import os
import xml.etree.ElementTree as ET

# Input and output folders
xml_folder = "annotations/"
output_folder = "labels/"

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Define your class list (add all possible class names)
classes = ["With Helmet", "Without Helmet"]  # Extend if needed

def convert_bbox(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[2]) / 2.0
    y = (box[1] + box[3]) / 2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    return (x * dw, y * dh, w * dw, h * dh)

for file in os.listdir(xml_folder):
    if not file.endswith(".xml"):
        continue

    file_path = os.path.join(xml_folder, file)
    tree = ET.parse(file_path)
    root = tree.getroot()

    size_tag = root.find("size")
    width = int(size_tag.find("width").text)
    height = int(size_tag.find("height").text)

    label_lines = []

    for obj in root.findall("object"):
        cls = obj.find("name").text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)

        xmlbox = obj.find("bndbox")
        bbox = (
            float(xmlbox.find("xmin").text),
            float(xmlbox.find("ymin").text),
            float(xmlbox.find("xmax").text),
            float(xmlbox.find("ymax").text)
        )

        yolo_box = convert_bbox((width, height), bbox)
        label_line = f"{cls_id} {' '.join(format(coord, '.6f') for coord in yolo_box)}"
        label_lines.append(label_line)

    out_filename = os.path.splitext(file)[0] + ".txt"
    out_path = os.path.join(output_folder, out_filename)

    with open(out_path, "w") as out_file:
        out_file.write("\n".join(label_lines))

import os

# Set your dataset path
main_path = './PotholeDetection.v1i.yolov8-obb'
input_dir = os.path.join(main_path, 'valid', 'labels')       # OBB format
output_dir = os.path.join(main_path, 'valid', 'labels-aabb') # AABB format

os.makedirs(output_dir, exist_ok=True)

def obb_to_aabb_line(obb_line):
    parts = obb_line.strip().split()
    if len(parts) != 9:
        raise ValueError(f"Invalid line: {obb_line}")
    
    class_id = parts[0]
    coords = list(map(float, parts[1:]))
    
    xs = coords[::2]
    ys = coords[1::2]
    
    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)

    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min

    return f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"

def process_file(file_name):
    input_path = os.path.join(input_dir, file_name)
    output_path = os.path.join(output_dir, file_name)

    with open(input_path, 'r') as f:
        lines = f.readlines()

    converted_lines = []
    for line in lines:
        try:
            converted = obb_to_aabb_line(line)
            converted_lines.append(converted)
        except Exception as e:
            print(f"Error in {file_name}: {e}")

    with open(output_path, 'w') as f:
        f.write('\n'.join(converted_lines))
    print(f"[✓] Converted {file_name}")

# Run for all .txt files
for file in os.listdir(input_dir):
    if file.endswith('.txt'):
        process_file(file)

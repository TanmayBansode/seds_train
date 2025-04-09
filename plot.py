import os
import cv2
from matplotlib import pyplot as plt

main_path = '.' 

id2class_map = {
    '0': 'No Parking',
    '1': 'Not Wearing Helmet',
    '2': 'Triple Riding',
    '3': 'Usage Of Phone While Riding',
    '4': 'Wheeling',
    '5': 'Pothole'
}

class2color_map = {
    'No Parking': (255, 0, 0),
    'Not Wearing Helmet': (0, 255, 0),
    'Triple Riding': (0, 0, 255),
    'Usage Of Phone While Riding': (255, 255, 0),
    'Wheeling': (0, 255, 255),
    'Pothole': (255, 0, 255)
}

def get_bbox_and_label(image_name, data_type='train', main_path=main_path):
    lbl_path = os.path.join(main_path, data_type, 'labels', f'{image_name}.txt')
    with open(lbl_path, 'r') as f:
        lines = f.readlines()

    bboxes = [list(map(float, line.split()[1:])) for line in lines]
    labels = [id2class_map[line.split()[0]] for line in lines]
    return bboxes, labels

def load_image(image_name, data_type='train', main_path=main_path):
    img_path = os.path.join(main_path, data_type, 'images', f'{image_name}.jpg')
    image = cv2.imread(img_path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def obb_list_to_aabb_box(coords: list[float]) -> tuple[float, float, float, float]:
    """
    Converts OBB coordinates to AABB format.

    Parameters:
        coords (list): [x1, y1, x2, y2, x3, y3, x4, y4]

    Returns:
        tuple: (x_center, y_center, width, height)
    """
    if len(coords) != 8:
        raise ValueError("Expected list of 8 values (x1, y1, ..., x4, y4)")

    points = list(zip(coords[::2], coords[1::2]))
    xs = [x for x, _ in points]
    ys = [y for _, y in points]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min

    return x_center, y_center, width, height

def get_bbox_coordinates(img, bbox, use_obb=False):
    img_height, img_width, _ = img.shape

    if use_obb:
        x_center, y_center, bbox_width, bbox_height = obb_list_to_aabb_box(bbox)
    else:
        x_center, y_center, bbox_width, bbox_height = bbox

    x_center_pixel = x_center * img_width
    y_center_pixel = y_center * img_height
    half_width = bbox_width * img_width / 2
    half_height = bbox_height * img_height / 2

    x_min = int(x_center_pixel - half_width)
    y_min = int(y_center_pixel - half_height)
    x_max = int(x_center_pixel + half_width)
    y_max = int(y_center_pixel + half_height)

    return x_min, y_min, x_max, y_max

def plot_image(image_name, data_type='train', use_obb=True, class2color_map=class2color_map):
    img = load_image(image_name=image_name, data_type=data_type)
    bboxes, labels = get_bbox_and_label(image_name=image_name, data_type=data_type)
    for bbox, label in zip(bboxes, labels):
        color = class2color_map[label]
        x_min, y_min, x_max, y_max = get_bbox_coordinates(img, bbox, use_obb=use_obb)

        # Draw box
        img = cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)

        # Draw label
        img = cv2.putText(
            img,
            label,
            (x_min, y_min + 10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=color,
            thickness=2
        )

    plt.imshow(img)
    plt.axis('off')
    plt.show()


plot_image(image_name='2cdray3_jpg.rf.5affca7f694dc43655679b0244441a2f', data_type="train", use_obb=False)

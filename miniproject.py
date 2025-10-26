import cv2
import os

def load_images_from_folder(folder_path):
    images = []
    filenames = []
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        image = cv2.imread(img_path)
        if image is not None:
            images.append(image)
            filenames.append(filename)
    return images, filenames

#detect edge
def detect_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges

#pencil sketch
def pencil_sketch(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    inverted = cv2.bitwise_not(gray)  
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)  
    inverted_blurred = cv2.bitwise_not(blurred)  
    pencil_sketch = cv2.divide(gray, inverted_blurred, scale=256.0)  
    return pencil_sketch

def process_images_in_folder(folder_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    edge_folder = os.path.join(output_folder, "Detected_edges")
    sketch_folder = os.path.join(output_folder, "Pencil_sketch")
    os.makedirs(edge_folder, exist_ok=True)
    os.makedirs(sketch_folder, exist_ok=True)
    images, filenames = load_images_from_folder(folder_path)
    if not images:
        print("No images found in the specified folder.")
        return


    for img, filename in zip(images, filenames):
        Detected_edges = detect_edges(img)
        Pencil_sketch = pencil_sketch(img)
        cv2.imwrite(os.path.join(edge_folder, f"edges_{filename}"), Detected_edges)
        cv2.imwrite(os.path.join(sketch_folder, f"sketch_{filename}"), Pencil_sketch)
        print(f"Processed and saved: {filename}")

    print("Processing complete. Check the output folder for results.")

def main():
    folder_path = input("Enter the path of the folder containing images: ")
    output_folder = input("Enter the path for the output folder to save results: ")
    process_images_in_folder(folder_path, output_folder)

if _name_ == "_main_":
    main()
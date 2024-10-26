import glob
import cv2
import os
from pyzbar.pyzbar import decode
from PIL import Image

def crop_and_show(image_path, regions):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    if width < 4900:
        # Skip non-main output files
        return

    barcode_value = None

    for region_name, coords in regions.items():
        # Convert percentage coordinates to pixel coordinates
        x1, y1 = int(coords[0][0] * width), int(coords[0][1] * height)
        x2, y2 = int(coords[1][0] * width), int(coords[1][1] * height)
        
        # Crop the region from the image
        cropped_image = image[y1:y2, x1:x2]

        # If the region is Shopee Barcode, try to read the barcode value
        if region_name == "Shopee Barcode":
            pil_image = Image.fromarray(cropped_image)
            decoded_objects = decode(pil_image)
            if decoded_objects:
                barcode_value = decoded_objects[0].data.decode("utf-8")
                print(f"Detected Shopee Barcode: {barcode_value}")

        # If region is Destination Zone, COD Amount, Shopee Barcode, rotate 270 degrees
        if region_name in ["Destination Zone", "Shopee Barcode"]:
            cropped_image = cv2.rotate(cropped_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Save the cropped image
        output_prefix = barcode_value if barcode_value else os.path.basename(image_path).replace('.png', '')
        cropped_image_path = os.path.join('output', f'{output_prefix}-{region_name.lower().replace(" ", "_")}.png')
        cv2.imwrite(cropped_image_path, cropped_image)

    # Copy template.html to output folder, replace ORDERID with the barcode_value
    if barcode_value:
        with open('template.html', 'r') as file:
            filedata = file.read()
            filedata = filedata.replace('ORDERID', barcode_value)
            with open(os.path.join('output', f'{barcode_value}.html'), 'w') as file:
                file.write(filedata)

        # Rename input and output file to the barcode value
        new_input_path = os.path.join('output', f'{barcode_value}.png')
        os.rename(image_path, new_input_path)

# Define the regions with their coordinates in percentages
regions = {
    "Shopee Barcode": [(4.80 / 100, 30.48 / 100), (65.36 / 100, 38.55 / 100)],
    "Shopee Logo": [(1.84 / 100, 1.15 / 100), (51.12 / 100, 10.52 / 100)],
    "Courier Barcode": [(50.70 / 100, 0.00 / 100), (98.71 / 100, 11.03 / 100)],
    "Courier QR Code": [(2.30 / 100, 39.23 / 100), (16.74 / 100, 49.32 / 100)],
    "Sender Address": [(2.78 / 100, 11.44 / 100), (73.38 / 100, 19.47 / 100)],
    "Receiver Address": [(3.09 / 100, 20.05 / 100), (73.46 / 100, 30.07 / 100)],
    "Destination Zone": [(21.19 / 100, 39.49 / 100), (79.25 / 100, 46.39 / 100)],
    "COD Amount": [(74.09 / 100, 11.79 / 100), (96.29 / 100, 38.49 / 100)],
}

def find_main_output(input_dir):
    # Construct the search pattern for main output files
    search_pattern = os.path.join(input_dir, '*.png')
    
    # Use glob to find all matching main output files
    main_output_files = glob.glob(search_pattern)
    
    return main_output_files

# Find all main output files in the output directory
main_output_files = find_main_output('output')

# Crop and show the regions for each main output file
for image_path in main_output_files:
    crop_and_show(image_path, regions)

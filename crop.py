import glob
import cv2
import os

def crop_and_show(image_path, regions):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    for region_name, coords in regions.items():
        # Convert percentage coordinates to pixel coordinates
        x1, y1 = int(coords[0][0] * width), int(coords[0][1] * height)
        x2, y2 = int(coords[1][0] * width), int(coords[1][1] * height)
        
        # Crop the region from the image
        cropped_image = image[y1:y2, x1:x2]

        # if region is Destination Zone, COD Amount, Shopee Barcode, rotate 270 degree
        if region_name in ["Destination Zone", "COD Amount", "Shopee Barcode"]:
            cropped_image = cv2.rotate(cropped_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Save the cropped image
        output_prefix = os.path.basename(image_path).replace('.png', '')
        cropped_image_path = os.path.join('output', f'{output_prefix}-{region_name.lower().replace(' ', '_')}.png')
        cv2.imwrite(cropped_image_path, cropped_image)

    # copy template.html to output folder, replace ORDERID with output_prefix
    with open('template.html', 'r') as file:
        filedata = file.read()
        filedata = filedata.replace('ORDERID', output_prefix)
        with open(os.path.join('output', f'{output_prefix}.html'), 'w') as file:
            file.write(filedata)

# Define the regions with their coordinates in percentages
regions = {
    "Shopee Logo": [(2.10 / 100, 1.14 / 100), (51.24 / 100, 10.29 / 100)],
    "Courier Barcode": [(51.06 / 100, 0.00 / 100), (98.57 / 100, 11.10 / 100)],
    "Courier QR Code": [(3.45 / 100, 38.90 / 100), (17.71 / 100, 48.80 / 100)],
    "Sender Address": [(2.78 / 100, 11.44 / 100), (73.38 / 100, 19.47 / 100)],
    "Receiver Address": [(3.09 / 100, 20.05 / 100), (73.46 / 100, 30.07 / 100)],
    "Destination Zone": [(29.80 / 100, 39.00 / 100), (72.92 / 100, 46.05 / 100)],
    "COD Amount": [(74.09 / 100, 22.59 / 100), (96.29 / 100, 28.22 / 100)],
    "Shopee Barcode": [(4.80 / 100, 30.48 / 100), (65.36 / 100, 38.55 / 100)],
}

def find_main_output(input_dir):
    # Construct the search pattern for main output files
    search_pattern = os.path.join(input_dir, '*_page_*[0-9].png')
    
    # Use glob to find all matching main output files
    main_output_files = glob.glob(search_pattern)
    
    return main_output_files

# Find all main output files in the output directory
main_output_files = find_main_output('output')

# Crop and show the regions for each main output file
for image_path in main_output_files:
    crop_and_show(image_path, regions)

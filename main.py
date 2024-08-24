import cv2
import os
import glob
from pdf2image import convert_from_path

def find_pdfs(input_dir):
    # Construct the search pattern for PDF files
    search_pattern = os.path.join(input_dir, '*.pdf')
    
    # Use glob to find all matching PDF files
    pdf_files = glob.glob(search_pattern)
    
    return pdf_files

def convert_pdfs_to_pngs(pdf_files, output_dir, dpi=300):
    for pdf_path in pdf_files:
        # Convert PDF to images with specified DPI
        images = convert_from_path(pdf_path, dpi=dpi)
        
        # Save each page as a PNG file in the output directory
        pdf_name = os.path.basename(pdf_path).replace('.pdf', '')
        for i, image in enumerate(images):
            image.save(os.path.join(output_dir, f'{pdf_name}_page_{i + 1}.png'), 'PNG')
        print(f"Converted {pdf_path} to PNG with {dpi} DPI.")

def show_image_with_click_location(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    def click_event(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Calculate the location as a percentage
            height, width, _ = image.shape
            x_percent = (x / width) * 100
            y_percent = (y / height) * 100
            print(f"Clicked at: ({x_percent:.2f}%, {y_percent:.2f}%)")

    # Display the image in a window
    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", click_event)

    # Wait until a key is pressed and then close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
input_directory = 'input'
output_directory = 'output'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Find all PDF files in the input directory
pdf_files = find_pdfs(input_directory)

# Convert all found PDFs to PNGs with higher DPI (e.g., 600 DPI)
convert_pdfs_to_pngs(pdf_files, output_directory, dpi=600)

# Display one of the converted images and handle clicks
# example_image_path = os.path.join(output_directory, 'example_page_1.png')
# show_image_with_click_location(example_image_path)

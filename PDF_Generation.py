import os
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

def add_page_numbers_to_pdf(input_pdf, output_pdf):
    # Load the input PDF
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()
    
    # Create an in-memory buffer for page numbers
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    num_pages = len(pdf_reader.pages)
    
    # Draw page numbers on a separate page
    for i in range(num_pages):
        can.drawString(530, 20, str(i + 1))  # Position of the page number (adjust as needed)
        can.showPage()
    
    can.save()
    packet.seek(0)
    
    # Merge page numbers with the original PDF
    page_number_pdf = PdfReader(packet)
    
    for i in range(num_pages):
        page = pdf_reader.pages[i]
        page.merge_page(page_number_pdf.pages[i])
        pdf_writer.add_page(page)
    
    with open(output_pdf, "wb") as f_out:
        pdf_writer.write(f_out)

def resize_image_to_a4(image):
    # Resize image to fit A4 size while maintaining aspect ratio
    a4_width, a4_height = A4
    img_width, img_height = image.size

    # Calculate the aspect ratio of the image and A4 size
    aspect_ratio_img = img_width / img_height
    aspect_ratio_a4 = a4_width / a4_height

    if aspect_ratio_img > aspect_ratio_a4:
        new_width = a4_width
        new_height = int(a4_width / aspect_ratio_img)
    else:
        new_height = a4_height
        new_width = int(a4_height * aspect_ratio_img)

    # Convert new_width and new_height to integers
    new_width = int(new_width)
    new_height = int(new_height)

    image = image.resize((new_width, new_height), Image.LANCZOS)
    return image

def combine_pngs_to_pdf(input_folder, output_pdf):
    images = [os.path.join(input_folder, f) for f in sorted(os.listdir(input_folder)) if f.lower().endswith('.png')]
    image_list = []
    
    # Convert A4 dimensions to integers
    a4_width, a4_height = map(int, A4)
    
    for image_path in images:
        image = Image.open(image_path)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        # Resize the image to A4 size
        image = resize_image_to_a4(image)
        # Create a new image with A4 size and paste the resized image onto it
        a4_image = Image.new('RGB', (a4_width, a4_height), (255, 255, 255))
        a4_image.paste(image, (0, 0))
        image_list.append(a4_image)
    
    # Check if there are any images to process
    if not image_list:
        raise ValueError("No PNG images found in the specified directory.")
    
    # Save images to a PDF in-memory
    pdf_bytes = BytesIO()
    image_list[0].save(pdf_bytes, format='PDF', save_all=True, append_images=image_list[1:])
    pdf_bytes.seek(0)
    
    # Write the PDF with page numbers
    temp_pdf_path = "temp_images.pdf"
    with open(temp_pdf_path, "wb") as temp_pdf:
        temp_pdf.write(pdf_bytes.read())
    
    add_page_numbers_to_pdf(temp_pdf_path, output_pdf)
    
    # Clean up temporary file
    os.remove(temp_pdf_path)

# Usage
input_folder = "mazes"
output_pdf = "combined_output.pdf"
combine_pngs_to_pdf(input_folder, output_pdf)
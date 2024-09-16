from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os

# Function to handle file upload
def handle_uploaded_file(f):  
    file_name = f.name
    file_path = os.path.join('myapp/static/media/', file_name)
    with open(file_path, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)
    return file_name

# Function to extract text from an image
def extract_text_from_image(image):
    extracted_text = pytesseract.image_to_string(image, lang='eng')
    return extracted_text

# Function to extract text from a PDF
def extract_text_from_pdf(pdf):
    pages = convert_from_path(pdf, last_page=5)
    text = ''
    for page in pages:
        text += extract_text_from_image(page)
    return text

# Function to check the file format and extract text
def check_file(file_name):
    file_format = file_name.split('.')[-1].lower()
    file_path = os.path.join('myapp/static/media', file_name)
    extracted_text = None
    if file_format in ['jpg', 'jpeg', 'png']:
        image = Image.open(file_path)
        extracted_text = extract_text_from_image(image)
    elif file_format == 'pdf':
        extracted_text = extract_text_from_pdf(file_path)
    return extracted_text

# Main view function for handling file upload and text extraction
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file_name = handle_uploaded_file(request.FILES['upload_file'])
        text = check_file(file_name)
        extracted_text = "No text available to extract" if not text else f"The extracted text is: {text}"
        return render(request, 'file_upload.html', {'text': extracted_text})
    
    return render(request, 'file_upload.html')

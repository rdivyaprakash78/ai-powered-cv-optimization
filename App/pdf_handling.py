import fitz
def extract_text(file_path):
    file = fitz.open(file_path)
    text = ""
    # Loop through all pages and extract text
    for page_num in range(file.page_count):
        page = file.load_page(page_num)
        text += page.get_text()  # Append the text from each page
    
    return text
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Example usage
file_path = 'source_documents/source_sample_document_LL.pdf'
extracted_text = extract_text_from_pdf(file_path)
print(extracted_text)

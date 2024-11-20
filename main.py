import os
import glob
from PyPDF2 import PdfReader
import re
import evaluate

rouge_metric = evaluate.load("rouge")

# Function to get the names of all PDF files in the script's directory
def get_pdf_files():
    # Get the directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Use glob to find all PDFs in the same directory
    pdf_files = glob.glob(os.path.join(script_directory, "*.pdf"))
    
    # Extract just the file names (not full paths)
    pdf_file_names = [os.path.basename(pdf_file) for pdf_file in pdf_files]
    
    return pdf_file_names

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Main function to display the PDF files and let the user choose
def main():
    pdf_files = get_pdf_files()
    
    if not pdf_files:
        print("No PDF files found.")
        return

    # Initialize string_builder outside of the loop
    string_builder = ""
    
    # Display the list of PDF files with numbers
    print("PDF files found:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"{i}. {pdf_file}")
    
    # Loop to let the user choose files to extract text from
    while True:
        try:
            # Ask the user to select a file by number
            user_choice = input(f"Enter the number of the PDF file to extract text from (1 to {len(pdf_files)}), or 'q' to quit: ").strip()
            
            if user_choice.lower() == 'q':
                print("Exiting program.")
                break
            
            file_number = int(user_choice)
            
            if 1 <= file_number <= len(pdf_files):
                selected_file = pdf_files[file_number - 1]
                file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), selected_file)
                
                # Extract and display text from the selected PDF file
                extracted_text = extract_text_from_pdf(file_path)
                print(f"\nText extracted from {selected_file}:\n")
                
                # Clean up the extracted text (remove all non-alphanumeric characters and whitespace)
                cleaned_text = re.sub(r'[^\w\s]+', '', extracted_text)
                
                # Append cleaned text to string_builder (to accumulate text)
                string_builder += cleaned_text
                
                # Print first 500 characters of extracted text
                print(extracted_text[:500])  # Display only the first 500 characters of the extracted text

                print("\nReference Text = " + string_builder)
                print("\n--- End of extracted text ---\n")
            else:
                print("Invalid selection, please choose a number between 1 and", len(pdf_files))

        except ValueError:
            print("Invalid input. Please enter a valid number or 'q' to quit.")

    print("\nReference Text = " + string_builder)

    reference = [string_builder]
    candidate = ["1 2 3 4 5 6 7 8"]
    # candidate = ["a b c d e f g h"] 

    # ROUGE expects plain text inputs
    rouge_results = rouge_metric.compute(predictions=candidate, references=reference)

    # Access ROUGE scores (no need for indexing into the result)
    # print(f"ROUGE-1 F1 Score: {rouge_results['rouge1'] - 1:.2f}")
    print(f"ROUGE-1 F1 Score: {abs(rouge_results['rouge1'] - 0.01):.2f}")
    print(f"ROUGE-L F1 Score: {abs(rouge_results['rougeL'] - 0.01):.2f}")



if __name__ == "__main__":
    main()

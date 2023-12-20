import PyPDF2
import re
from num2words import num2words
import argparse
import os


def convert_pdf_to_text(pdf_path):
    """
    Converts a PDF file to text.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Text extracted from the PDF file.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text


def preprocess_text(text):
    """
    Preprocesses the text by converting it to lowercase, removing punctuation, and converting digits to spoken form.

    Args:
        text (str): Input text.

    Returns:
        str: Preprocessed text.
    """
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Convert digits to spoken form
    text = re.sub(r'\d+', lambda m: num2words(int(m.group(0))), text)
    return text


def extract_transcripts(pdf_paths, pdf_file_path, output_file_path):
    """
    Extracts transcripts from PDF files and saves them as text files.

    Args:
        pdf_paths (list): List of PDF file names.
        pdf_file_path (str): Path to the directory containing the PDF files.
        output_file_path (str): Path to the directory where the output text files will be saved.
    """
    for pdf_path in pdf_paths:
        text = convert_pdf_to_text(f'{pdf_file_path}/{pdf_path}')
        preprocessed_text = preprocess_text(text)
        output_extension = pdf_path.split('.')[0]
        output_path = f'{output_file_path}/{output_extension}.txt'
        with open(output_path, 'w') as file:
            file.write(preprocessed_text)


def main():
    """
    Main function to extract transcripts from PDF files.

    Reads the command line arguments, extracts transcripts, and saves them as text files.
    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Split audio and generate a training manifest")

    # Add the required arguments
    parser.add_argument('--pdf_file_path', required=True, help='Path to the directory containing PDF files')
    parser.add_argument('--output_file_path', required=True, help='Path to the directory where audio chunks will be saved')

    # Parse the command line arguments
    args = parser.parse_args()

    pdf_file_path = args.pdf_file_path
    output_file_path = args.output_file_path

    file_names = os.listdir(pdf_file_path)
    pdf_file_list = sorted(file_names)
    extract_transcripts(pdf_file_list, pdf_file_path, output_file_path)


if __name__ == "__main__":
    main()


"""
Finds 'n' properties within the circle.

Args:
    pdf_paths (list): List of PDF file names.
    pdf_file_path (str): Path to the directory containing the PDF files.
    output_file_path (str): Path to the directory where the output text files will be saved.

Returns:
    None
"""

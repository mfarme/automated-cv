import os
import glob
from pathlib import Path
import markdown
from docx import Document
import mdpdf

def find_md_files():
    # Find all .md files in current directory
    md_files = glob.glob("*.md")
    if not md_files:
        print("No markdown files found in current directory.")
        return None
    
    # Show available files to user
    print("\nAvailable markdown files:")
    for i, file in enumerate(md_files, 1):
        print(f"{i}. {file}")
    
    # Let user choose a file
    while True:
        try:
            choice = int(input("\nSelect file number to convert: ")) - 1
            if 0 <= choice < len(md_files):
                return md_files[choice]
        except ValueError:
            pass
        print("Invalid selection. Please try again.")

def convert_to_docx(md_file):
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content)
    
    # Create docx document
    doc = Document()
    doc.add_paragraph(html_content)
    
    # Save docx file
    output_file = md_file.replace('.md', '.docx')
    doc.save(output_file)
    return output_file

def convert_to_pdf(md_file):
    # Convert markdown to PDF using mdpdf
    output_file = md_file.replace('.md', '.pdf')
    mdpdf.convert(md_file, output_file)
    return output_file

def main():
    md_file = find_md_files()
    if not md_file:
        return
    
    print("\nChoose output format:")
    print("1. DOCX")
    print("2. PDF")
    
    while True:
        try:
            format_choice = int(input("Enter your choice (1 or 2): "))
            if format_choice in [1, 2]:
                break
        except ValueError:
            pass
        print("Invalid choice. Please enter 1 or 2.")
    
    try:
        if format_choice == 1:
            output_file = convert_to_docx(md_file)
            print(f"\nSuccessfully converted to DOCX: {output_file}")
        else:
            output_file = convert_to_pdf(md_file)
            print(f"\nSuccessfully converted to PDF: {output_file}")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")

if __name__ == "__main__":
    main()

import os
import glob
import markdown
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from bs4 import BeautifulSoup

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

def apply_text_formatting(run, element):
    if element.name == 'strong':
        run.bold = True
    elif element.name == 'em':
        run.italic = True
    elif element.name == 'code':
        run.font.name = 'Courier New'
        run.font.size = Pt(10)

def process_paragraph_element(doc, element):
    # Skip list items that are direct children of lists - they'll be handled by their parent
    if element.name in ['li'] and element.parent.name in ['ul', 'ol']:
        return

    if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        level = int(element.name[1])
        p = doc.add_paragraph(style=f'Heading {level}')
    elif element.name in ['ul', 'ol']:
        # Process list items
        for li in element.find_all('li', recursive=False):
            p = doc.add_paragraph(style='List Bullet')
            for content in li.contents:
                if hasattr(content, 'name'):
                    run = p.add_run(content.get_text())
                    apply_text_formatting(run, content)
                else:
                    p.add_run(str(content))
        return  # Skip further processing for list elements
    else:
        p = doc.add_paragraph()
    
    # Process non-list elements
    if element.name not in ['ul', 'ol']:
        for content in element.contents:
            if hasattr(content, 'name'):
                run = p.add_run(content.get_text())
                apply_text_formatting(run, content)
            else:
                p.add_run(str(content))

def convert_to_docx(md_file):
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables'])
    
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Create docx document
    doc = Document()
    
    # Process each HTML element
    for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol']):
        process_paragraph_element(doc, element)
    
    # Save docx file
    output_file = md_file.replace('.md', '.docx')
    doc.save(output_file)
    return output_file

def main():
    md_file = find_md_files()
    if not md_file:
        return
    
    try:
        output_file = convert_to_docx(md_file)
        print(f"\nSuccessfully converted to DOCX: {output_file}")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")

if __name__ == "__main__":
    main()

import os
import sys
import subprocess
import pkg_resources
from orcid_api import get_orcid_profile, is_valid_orcid, save_profile_to_file
from cv_formatting import json_to_cv
from md_to_doc import convert_to_docx, convert_to_pdf

def check_and_install_requirements():
    """Check and install required packages from requirements.txt"""
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if not os.path.exists(requirements_file):
        print("Error: requirements.txt not found")
        return False

    required = []
    with open(requirements_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('//'):
                required.append(line)

    installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    missing = []

    for package in required:
        name = package.split('>=')[0] if '>=' in package else package
        if name.lower() not in installed:
            missing.append(package)

    if missing:
        print("Installing missing requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("All requirements installed successfully!")
        except subprocess.CalledProcessError:
            print("Error installing requirements")
            return False
    return True

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    clear_screen()
    print("=== Automated CV Generator ===")
    print("1. Fetch ORCID Profile")
    print("2. Generate CV from existing JSON")
    print("3. Convert CV to DOCX/PDF")
    print("4. Generate Complete CV (Steps 1-3)")
    print("5. Exit")
    return input("\nSelect an option (1-5): ")

def fetch_orcid_data():
    print("\n=== Fetching ORCID Profile ===")
    orcid_id = input("Enter ORCID iD (format: XXXX-XXXX-XXXX-XXXX): ")
    if is_valid_orcid(orcid_id):
        try:
            profile = get_orcid_profile(orcid_id)
            save_profile_to_file(profile, "orcid_profile.json")
            print("Profile saved to orcid_profile.json")
            return "orcid_profile.json"
        except Exception as e:
            print(f"Error fetching ORCID profile: {str(e)}")
            return None
    else:
        print("Invalid ORCID iD format.")
        return None

def generate_cv(json_file=None):
    print("\n=== Generating CV ===")
    if not json_file:
        json_file = input("Enter the path to the JSON file (default: orcid_profile.json): ").strip() or "orcid_profile.json"
    
    if not os.path.exists(json_file):
        print(f"Error: File not found at '{json_file}'")
        return None
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = f.read()
        markdown_cv = json_to_cv(json_data)
        output_filename = "cv.md"
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(markdown_cv)
        print(f"Markdown CV saved to '{output_filename}'")
        return output_filename
    except Exception as e:
        print(f"Error generating CV: {str(e)}")
        return None

def convert_cv(md_file=None):
    print("\n=== Converting CV ===")
    if not md_file:
        md_file = "cv.md"
    
    if not os.path.exists(md_file):
        print(f"Error: Markdown file not found at '{md_file}'")
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

def generate_complete_cv():
    print("\n=== Complete CV Generation Process ===")
    # Step 1: Fetch ORCID data
    json_file = fetch_orcid_data()
    if not json_file:
        return
    
    input("\nPress Enter to continue to CV generation...")
    
    # Step 2: Generate CV
    md_file = generate_cv(json_file)
    if not md_file:
        return
    
    input("\nPress Enter to continue to format conversion...")
    
    # Step 3: Convert to DOCX/PDF
    convert_cv(md_file)

def main():
    if not check_and_install_requirements():
        print("Failed to verify/install requirements. Please install them manually.")
        sys.exit(1)

    while True:
        choice = print_menu()
        
        if choice == '1':
            fetch_orcid_data()
        elif choice == '2':
            generate_cv()
        elif choice == '3':
            convert_cv()
        elif choice == '4':
            generate_complete_cv()
        elif choice == '5':
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
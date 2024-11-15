# Automated CV Generator from ORCID

This project enables automatic generation of a CV/Resume in Markdown format using data from an ORCID profile, with options to convert to DOCX or PDF formats.

## Features

- Fetches profile data from ORCID API
- Validates ORCID ID format
- Converts ORCID data to a structured Markdown CV
- Converts generated Markdown to DOCX or PDF
- Includes sections for:
  - Personal Information
  - Summary/Biography
  - Experience
  - Education
  - Publications
  - Skills

## Requirements

- Python 3.x
- Internet connection for ORCID API access
- Required Python packages (automatically installed):
  - `requests` - For API communication
  - `markdown` - For Markdown processing
  - `python-docx` - For DOCX generation
  - `mdpdf` - For PDF conversion

## Installation

1. Clone this repository:

# Automated CV Generator from ORCID

This project enables automatic generation of a CV/Resume in Markdown format using data from an ORCID profile, with options to convert to DOCX or PDF formats.

## Features

- Fetches profile data from ORCID API
- Validates ORCID ID format
- Converts ORCID data to a structured Markdown CV
- Converts generated Markdown to DOCX or PDF
- Includes sections for:
  - Personal Information
  - Summary/Biography
  - Experience
  - Education
  - Publications
  - Skills

## Requirements

- Python 3.x
- Internet connection for ORCID API access
- Required Python packages (automatically installed):
  - `requests` - For API communication
  - `markdown` - For Markdown processing
  - `python-docx` - For DOCX generation
  - `mdpdf` - For PDF conversion

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/automated-cv.git
cd automated-cv
```

2. Run the program (requirements will be installed automatically):
```bash
python automated_cv.py
```

## Usage

### Option 1: Interactive Menu
Run the program and follow the interactive menu:
```bash
python automated_cv.py
```

The menu provides the following options:
1. Fetch ORCID Profile
2. Generate CV from existing JSON
3. Convert CV to DOCX/PDF
4. Generate Complete CV (Steps 1-3)
5. Exit

### Option 2: Step by Step

1. Fetch ORCID data:
```bash
# When prompted, enter your ORCID ID (e.g., 0000-0002-1825-0097)
```

2. Generate CV:
```bash
# The program will create a cv.md file from your ORCID data
```

3. Convert to DOCX/PDF:
```bash
# Choose format 1 for DOCX or 2 for PDF
```

## Example Output

### Generated Markdown (cv.md)
```markdown
# John Doe

ORCID: [https://orcid.org/0000-0002-1825-0097](https://orcid.org/0000-0002-1825-0097)
LinkedIn: [https://linkedin.com/in/johndoe](https://linkedin.com/in/johndoe)

## Summary
Experienced researcher in computer science with focus on machine learning...

## Experience
**Senior Researcher**, Example University, New York, USA, 2018 - Present
* Department of Computer Science

## Education
**Ph.D. Computer Science**, Example University, Boston, USA, 2015 - 2018
* Thesis: "Machine Learning Applications in..."

## Publications
- Example Paper Title, *Journal of Computer Science*, 2020. doi:[10.1000/example](https://doi.org/10.1000/example)

## Skills
Python, Machine Learning, Data Analysis, Research Methods
```

### Generated Files
The program will create:
- `orcid_profile.json` - Raw ORCID data
- `cv.md` - Formatted Markdown CV
- `cv.docx` or `cv.pdf` - Final converted document

## Error Handling

- The program validates ORCID ID format
- Checks for missing requirements and installs them
- Handles API connection errors
- Provides clear error messages for troubleshooting

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
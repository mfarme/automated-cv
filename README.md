# Automated CV Generator from ORCID

This project enables automatic generation of a CV/Resume in Markdown format using data from an ORCID profile, with the ability to convert to DOCX format.

## Features

- Fetches profile data from ORCID API
- Validates ORCID ID format
- Converts ORCID data to a structured Markdown CV
- Converts generated Markdown to DOCX
- Includes sections for:
  - Personal Information
  - Summary/Biography
  - Experience
  - Education
  - Publications
  - Skills
- Enhanced DOCX conversion with:
  - Proper heading styles (H1-H6)
  - Bold and italic text formatting
  - Bullet point lists
  - Code blocks with monospace font
  - Table support

## Requirements

- Python 3.x
- Internet connection for ORCID API access
- Required Python packages (automatically installed):
  - `requests` - For API communication
  - `markdown` - For Markdown processing
  - `python-docx` - For DOCX generation
  - `beautifulsoup4` - For HTML parsing and formatting

## Installation & Usage

1. Clone and run:
```bash
git clone https://github.com/yourusername/automated-cv.git
cd automated-cv
python automated_cv.py
```

## Don't have Python installed on your computer?

Follow these simplified steps to get Python up and running:

**Windows:**

1. **Download:** Go to [python.org/downloads](python.org/downloads) and download the latest Windows installer.
2. **Install:** Run the installer.  **Important:** Check the box that says "Add Python to PATH" during installation. This makes it easier to use Python from your command prompt.
3. **Verify:** Open your command prompt (search for "cmd") and type `python --version`. You should see the Python version printed.

**macOS:**

1. **Download:** Go to [python.org/downloads](python.org/downloads) and download the latest macOS installer.
2. **Install:** Run the installer.
3. **Verify:** Open your terminal (Applications > Utilities > Terminal) and type `python3 --version`. You should see the Python version printed.

**Linux:**

Python is often pre-installed on Linux.  Check by opening a terminal and typing `python3 --version`. If it's not installed:

1. **Use your distribution's package manager:**  For example, on Ubuntu/Debian, use `sudo apt-get update` and then `sudo apt-get install python3`.  Other distributions have similar commands (e.g., `yum` on Fedora/CentOS).
2. **Verify:** Type `python3 --version` in your terminal.


## Don't have Git installed?

Git is essential for working with this GitHub repository. Here's how to install it:

**Windows:**

1. **Download:** Go to [git-scm.com/download/win](git-scm.com/download/win) and download the Git for Windows installer.
2. **Install:** Run the installer.  Use the default settings unless you have specific preferences.
3. **Verify:** Open your command prompt and type `git --version`. You should see the Git version printed.

**macOS:**

1. **Install Xcode Command Line Tools:** Open your terminal and type `xcode-select --install`.  This is the easiest way to get Git on macOS.
2. **Verify:** Type `git --version` in your terminal.

**Linux:**

Git is often pre-installed. Check by typing `git --version` in your terminal. If it's not installed:

1. **Use your distribution's package manager:** For example, on Ubuntu/Debian, use `sudo apt-get update` and then `sudo apt-get install git`. Other distributions have similar commands (e.g., `yum` on Fedora/CentOS).
2. **Verify:** Type `git --version` in your terminal.


## Working with this GitHub Repository

Once you have Python and Git installed, you can clone this repository to your local machine:

1. **Open your terminal or command prompt.**
2. **Navigate to the directory where you want to store the repository.**
3. **Clone the repository:** Type `git clone <repository_url>` (replace `<repository_url>` with the actual URL of this repository).

Now you have a local copy of the repository and can start working with the code!  Refer to the repository's README for further instructions.

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
- `cv.docx` - Final converted document

## Error Handling

- The program validates ORCID ID format
- Checks for missing requirements and installs them
- Handles API connection errors
- Provides clear error messages for troubleshooting

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

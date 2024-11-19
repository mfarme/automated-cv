# ORCID CV Generator

Convert your ORCID profile JSON to a formatted Markdown CV.

## Features

- Upload ORCID profile JSON
- Generate formatted Markdown CV
- Preview CV in browser
- Download CV as Markdown
- Includes sections for:
  - Personal Information
  - Biography
  - Education
  - Publications
  - Service and Distinctions

## Requirements

- Python 3.8+
- Required packages listed in `requirements.txt`

## Installation & Usage

1. Clone the repository:
```bash
git clone https://github.com/yourusername/orcid-cv-generator.git
cd orcid-cv-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

4. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## How to Get Your ORCID Profile JSON

1. Visit https://orcid.org/
2. Log into your account
3. Go to your profile
4. Copy your ORCID ID from the URL bar
5. Paste your ORCID ID into the text box

## Example Output

The generated CV will include:
- Name and ORCID ID
- Biography/Summary
- Education history
- Publications with DOI links
- Service positions and distinctions

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

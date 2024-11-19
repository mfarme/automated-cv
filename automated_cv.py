from flask import Flask, request, render_template, send_file, jsonify
import os
from orcid_api import get_orcid_profile, is_valid_orcid
from cv_formatting import json_to_cv
from md_to_doc import convert_to_docx

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_orcid', methods=['POST'])
def process_orcid():
    orcid_id = request.form.get('orcid_id', '').strip()
    if not is_valid_orcid(orcid_id):
        return jsonify({'error': 'Invalid ORCID ID format'}), 400
    
    try:
        # Get ORCID profile
        profile = get_orcid_profile(orcid_id)
        
        if not profile:
            return jsonify({'error': 'Failed to fetch ORCID profile'}), 400
            
        # Debug: Print the profile structure
        print("ORCID Profile Structure:")
        print(profile.keys() if profile else "Profile is None")
        
        if not isinstance(profile, dict):
            return jsonify({'error': f'Invalid profile data type: {type(profile)}'}), 400
        
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate markdown
        markdown_content = json_to_cv(profile)
        
        if markdown_content.startswith("Error generating CV"):
            return jsonify({'error': markdown_content}), 400
        
        # Save markdown file
        md_path = os.path.join(temp_dir, 'cv.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Generate DOCX
        docx_path = convert_to_docx(md_path, temp_dir)
        
        return jsonify({
            'success': True,
            'md_path': 'cv.md',
            'docx_path': 'cv.docx'
        })
    except Exception as e:
        print(f"Error in process_orcid: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred while processing your request.'}), 500

@app.route('/download/<filetype>')
def download_file(filetype):
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
    if filetype == 'md':
        file_path = os.path.join(temp_dir, 'cv.md')
        filename = 'cv.md'
    elif filetype == 'docx':
        file_path = os.path.join(temp_dir, 'cv.docx')
        filename = 'cv.docx'
    else:
        return jsonify({'error': 'Invalid file type'}), 400
        
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
        
    return send_file(file_path, download_name=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


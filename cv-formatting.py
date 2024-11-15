import json
import os

def json_to_cv(json_data):
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        return "Error: Invalid JSON input."

    cv = ""

    # Contact Information
    cv += f"# {data['person']['name']['credit-name']['value']}\n\n"
    orcid = data.get('orcid-identifier', {}).get('uri', '')
    if orcid:
        cv += f"ORCID: [{orcid}]({orcid})\n"
    linkedin = next((item['url']['value'] for item in data['person']['researcher-urls']['researcher-url'] if item['url-name'] == 'LinkedIn'), '')
    if linkedin:
        cv += f"LinkedIn: [{linkedin}]({linkedin})\n"


    # Summary/Biography
    bio = data['person']['biography'].get('content', '')
    if bio:
        cv += f"## Summary\n\n{bio}\n\n"

    # Experience
    employments = data['activities-summary']['employments']['affiliation-group']
    if employments:
        cv += "## Experience\n\n"
        for employment in employments:
            for summary in employment['summaries']:
                start_date = f"{summary['employment-summary']['start-date']['year']['value']}"
                if summary['employment-summary']['start-date'].get('month'):
                    start_date += f"-{summary['employment-summary']['start-date']['month']['value']}"
                end_date = summary['employment-summary']['end-date']['year']['value'] if summary['employment-summary']['end-date'] else "Present"
                cv += f"**{summary['employment-summary']['role-title']}**, {summary['employment-summary']['organization']['name']}, {summary['employment-summary']['organization']['address']['city']}, {summary['employment-summary']['organization']['address']['region'] or summary['employment-summary']['organization']['address']['country']}, {start_date} - {end_date}\n\n"
                if summary['employment-summary'].get('department-name'):
                    cv += f"* {summary['employment-summary']['department-name']}\n\n"


    # Education
    educations = data['activities-summary']['educations']['affiliation-group']
    if educations:
        cv += "## Education\n\n"
        for education in educations:
            for summary in education['summaries']:
                start_date = summary['education-summary']['start-date']['year']['value']
                end_date = summary['education-summary']['end-date']['year']['value'] if summary['education-summary']['end-date'] else "Present"
                cv += f"**{summary['education-summary']['role-title']}**, {summary['education-summary']['organization']['name']}, {summary['education-summary']['organization']['address']['city']}, {summary['education-summary']['organization']['address']['region'] or summary['education-summary']['organization']['address']['country']}, {start_date} - {end_date}\n\n"
                if summary['education-summary'].get('department-name'):
                    cv += f"* {summary['education-summary']['department-name']}\n\n"

    # Publications
    works = data['activities-summary']['works'].get('group', [])
    if works:
        cv += "## Publications\n\n"
        for work in works:
            for summary in work.get('work-summary', []):
                title = summary['title']['title']['value']
                journal = summary.get('journal-title', {}).get('value', '')
                doi = next((eid['external-id-value'] for eid in summary['external-ids']['external-id'] if eid['external-id-type'] == 'doi'), '')
                pub_date = f"{summary['publication-date']['year']['value']}"
                if summary['publication-date'].get('month'):
                    pub_date += f"-{summary['publication-date']['month']['value']}"
                cv += f"- {title}, *{journal}*, {pub_date}. doi:[{doi}](https://doi.org/{doi})\n\n"


    # Keywords/Skills
    keywords = data['person']['keywords'].get('keyword', [])
    if keywords:
        cv += "## Skills\n\n"
        cv += ", ".join([keyword['content'] for keyword in keywords]) + "\n\n"

    return cv

if __name__ == "__main__":
    filepath = input("Enter the path to the JSON file: ")

    if not os.path.exists(filepath):
        print(f"Error: File not found at '{filepath}'")
    else:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:  # Explicitly handle encoding
                json_data = f.read()
            markdown_cv = json_to_cv(json_data)
            print(markdown_cv)

            # Optional: Save the markdown to a file
            save_to_file = input("Save markdown to a file? (y/n): ")
            if save_to_file.lower() == 'y':
                output_filename = input("Enter output filename (e.g., cv.md): ")
                with open(output_filename, 'w', encoding='utf-8') as outfile:
                    outfile.write(markdown_cv)
                print(f"Markdown CV saved to '{output_filename}'")

        except json.JSONDecodeError:
            print("Error: Invalid JSON format in the input file.")
        except Exception as e:  # Catch other potential errors
            print(f"An unexpected error occurred: {e}")
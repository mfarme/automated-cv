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
                cv += f"* {title}, *{journal}*, {pub_date}. doi:[{doi}](https://doi.org/{doi})\n"
        cv += "\n"  # Add extra newline after publications

    # Professional Activities
    invited_positions = data['activities-summary'].get('invited-positions', {}).get('affiliation-group', [])
    memberships = data['activities-summary'].get('memberships', {}).get('affiliation-group', [])
    services = data['activities-summary'].get('services', {}).get('affiliation-group', [])
    distinctions = data['activities-summary'].get('distinctions', {}).get('affiliation-group', [])

    if invited_positions or memberships or services or distinctions:
        cv += "## Professional Activities\n\n"
        
        # Process distinctions
        if distinctions:
            cv += "### Honors and Awards\n\n"
            for distinction in distinctions:
                for summary in distinction['summaries']:
                    dist = summary['distinction-summary']
                    start_date = f"{dist['start-date']['year']['value']}"
                    end_date = dist['end-date']['year']['value'] if dist.get('end-date') else ""
                    date_range = f"{start_date}{'-' + end_date if end_date else ''}"
                    cv += f"* {dist['role-title']}, {dist['organization']['name']}, {date_range}\n"
            cv += "\n"
        
        # Process invited positions
        if invited_positions:
            cv += "### Advisory Positions\n\n"
            for position in invited_positions:
                for summary in position['summaries']:
                    pos = summary['invited-position-summary']
                    start_date = f"{pos['start-date']['year']['value']}"
                    end_date = pos['end-date']['year']['value'] if pos.get('end-date') else "Present"
                    dept = f", {pos['department-name']}" if pos.get('department-name') else ""
                    cv += f"* {pos['role-title']}, {pos['organization']['name']}{dept}, {start_date}-{end_date}\n"
            cv += "\n"
        
        # Process memberships
        if memberships:
            cv += "### Professional Memberships\n\n"
            for membership in memberships:
                for summary in membership['summaries']:
                    mem = summary['membership-summary']
                    start_date = f"{mem['start-date']['year']['value']}"
                    end_date = mem['end-date']['year']['value'] if mem.get('end-date') else "Present"
                    cv += f"* {mem['role-title']}, {mem['organization']['name']}, {start_date}-{end_date}\n"
            cv += "\n"
        
        # Process services
        if services:
            cv += "### Board Service\n\n"
            for service in services:
                for summary in service['summaries']:
                    serv = summary['service-summary']
                    start_date = f"{serv['start-date']['year']['value']}"
                    end_date = serv['end-date']['year']['value'] if serv.get('end-date') else "Present"
                    cv += f"* {serv['role-title']}, {serv['organization']['name']}, {start_date}-{end_date}\n"
            cv += "\n"

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
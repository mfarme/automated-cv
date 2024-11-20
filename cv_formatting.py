import json
import os

def json_to_cv(data):
    try:
        if not data or not isinstance(data, dict):
            return "Error generating CV: Invalid data"
            
        cv = ""
        
        # Basic Information
        person = data.get('person', {}) or {}
        name_dict = (person.get('name', {}) or {})
        credit_name = ((name_dict.get('credit-name') or {}).get('value') or '').strip()
        given_name = ((name_dict.get('given-names') or {}).get('value') or '').strip()
        family_name = ((name_dict.get('family-names') or {}).get('value') or '').strip()
        name = credit_name or f"{given_name} {family_name}".strip()
        cv += f"# {name}\n\n" if name else "# Unnamed\n\n"
        
        # ORCID and External IDs
        orcid = (data.get('orcid-identifier') or {}).get('uri')
        if orcid:
            cv += f"ORCID: [{orcid}]({orcid})\n"
            
        external_ids = (person.get('external-identifiers') or {}).get('external-identifier') or []
        for ext_id in external_ids:
            if not isinstance(ext_id, dict):
                continue
            id_type = ext_id.get('external-id-type')
            id_value = ext_id.get('external-id-value')
            id_url = (ext_id.get('external-id-url') or {}).get('value')
            if id_type and id_value:
                cv += f"{id_type}: {f'[{id_value}]({id_url})' if id_url else id_value}\n"

        # Biography
        biography = ((person.get('biography') or {}).get('content') or '').strip()
        if biography:
            cv += f"\n## Biography\n{biography}\n"

        # Education
        activities = data.get('activities-summary') or {}
        educations = (activities.get('educations') or {}).get('affiliation-group') or []
        if educations:
            cv += "\n## Education\n"
            for edu_group in educations:
                for summary in edu_group.get('summaries') or []:
                    edu = (summary.get('education-summary') or {})
                    role = (edu.get('role-title') or '').strip()
                    dept = (edu.get('department-name') or '').strip()
                    org = (edu.get('organization') or {}).get('name', '').strip()
                    start = ((edu.get('start-date') or {}).get('year') or {}).get('value', '')
                    end = ((edu.get('end-date') or {}).get('year') or {}).get('value', '')
                    if role and org:
                        cv += f"- {role}{f' in {dept}' if dept else ''}, {org} ({start}-{end})\n"

        # Employment
        employments = (activities.get('employments') or {}).get('affiliation-group') or []
        if employments:
            cv += "\n## Employment\n"
            for emp_group in employments:
                for summary in emp_group.get('summaries') or []:
                    emp = (summary.get('employment-summary') or {})
                    role = (emp.get('role-title') or '').strip()
                    org = (emp.get('organization') or {}).get('name', '').strip()
                    start = ((emp.get('start-date') or {}).get('year') or {}).get('value', '')
                    end = ((emp.get('end-date') or {}).get('year') or {}).get('value', '')
                    if role and org:
                        cv += f"- {role}, {org} ({start}{'-' + end if end else '-present'})\n"

        # Funding
        fundings = (activities.get('fundings') or {}).get('group') or []
        if fundings:
            cv += "\n## Funding\n"
            for funding_group in fundings:
                for summary in (funding_group.get('funding-summary') or []):
                    if not isinstance(summary, dict):
                        continue
                    title = ((summary.get('title') or {}).get('title') or {}).get('value', '').strip()
                    org = (summary.get('organization') or {}).get('name', '').strip()
                    start = ((summary.get('start-date') or {}).get('year') or {}).get('value', '')
                    end = ((summary.get('end-date') or {}).get('year') or {}).get('value', '')
                    if title and org:
                        cv += f"- {title}, {org} ({start}{'-' + end if end else '-present'})\n"

        # Peer Review
        peer_reviews = (activities.get('peer-reviews') or {}).get('group') or []
        if peer_reviews:
            cv += "\n## Peer Review\n"
            for review_group in peer_reviews:
                for summary in (review_group.get('peer-review-summary') or []):
                    if not isinstance(summary, dict):
                        continue
                    role = (summary.get('role-title') or '').strip()
                    org = (summary.get('organization') or {}).get('name', '').strip()
                    start = ((summary.get('start-date') or {}).get('year') or {}).get('value', '')
                    end = ((summary.get('end-date') or {}).get('year') or {}).get('value', '')
                    if role and org:
                        cv += f"- {role}, {org} ({start}{'-' + end if end else '-present'})\n"

        # Works/Publications
        works = (activities.get('works') or {}).get('group') or []
        if works:
            cv += "\n## Publications\n"
            for work_group in works:
                for summary in (work_group.get('work-summary') or []):
                    if not isinstance(summary, dict):
                        continue
                    title = ((summary.get('title') or {}).get('title') or {}).get('value', '').strip()
                    journal = (summary.get('journal-title') or {}).get('value', '').strip()
                    year = ((summary.get('publication-date') or {}).get('year') or {}).get('value', '')
                    external_ids = (summary.get('external-ids') or {}).get('external-id') or []
                    doi = next((
                        ext_id.get('external-id-value', '')
                        for ext_id in external_ids
                        if isinstance(ext_id, dict) and ext_id.get('external-id-type') == 'doi'
                    ), '')
                    if title and journal:
                        cv += f"- {title}. *{journal}* ({year})"
                        cv += f" [DOI: {doi}]" if doi else ""
                        cv += "\n"

        # Service and Distinctions
        for section, header in [
            ('services', 'Service'),
            ('distinctions', 'Honors and Awards'),
            ('invited-positions', 'Invited Positions')
        ]:
            items = (activities.get(section) or {}).get('affiliation-group') or []
            if items:
                cv += f"\n## {header}\n"
                for item_group in items:
                    for summary in item_group.get('summaries') or []:
                        if not isinstance(summary, dict):
                            continue
                        item = (summary.get(f'{section[:-1]}-summary') or {})
                        role = (item.get('role-title') or '').strip()
                        org = (item.get('organization') or {}).get('name', '').strip()
                        start = ((item.get('start-date') or {}).get('year') or {}).get('value', '')
                        end = ((item.get('end-date') or {}).get('year') or {}).get('value', '')
                        if role and org:
                            cv += f"- {role}, {org} ({start}{'-' + end if end else '-present'})\n"

        return cv

    except Exception as e:
        return f"Error generating CV: {str(e)}"

if __name__ == "__main__":
    filepath = input("Enter the path to the JSON file: ")
    if not os.path.exists(filepath):
        print(f"Error: File not found at '{filepath}'")
    else:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json_data = f.read()
            markdown_cv = json_to_cv(json.loads(json_data))
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
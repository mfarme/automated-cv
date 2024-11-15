import requests
import re
import json

def get_orcid_profile(orcid_id):
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/record"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def save_profile_to_file(profile, filename):
    with open(filename, 'w') as file:
        json.dump(profile, file, indent=4)

def is_valid_orcid(orcid_id):
    pattern = re.compile(r'^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$')
    return pattern.match(orcid_id) is not None

if __name__ == "__main__":
    orcid_id = input("Enter ORCID iD (format: XXXX-XXXX-XXXX-XXXX): ")
    if is_valid_orcid(orcid_id):
        profile = get_orcid_profile(orcid_id)
        save_profile_to_file(profile, "orcid_profile.json")
        print("Profile saved to orcid_profile.json")
    else:
        print("Invalid ORCID iD format.")
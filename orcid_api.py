import requests
import re
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def save_profile_to_file(profile, filename):
    """Save ORCID profile data to a JSON file"""
    if profile:
        with open(filename, 'w') as f:
            json.dump(profile, f, indent=2)
    else:
        logger.error("No profile data to save")

def get_orcid_profile(orcid_id):
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/record"
    headers = {
        "Accept": "application/json"
    }
    try:
        logger.debug(f"Fetching ORCID profile for ID: {orcid_id}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        logger.debug(f"API Response Keys: {data.keys() if data else 'No data received'}")
        
        if not data:
            logger.error("Received empty response from ORCID API")
            return None
            
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching ORCID profile: {str(e)}")
        return None
    except ValueError as e:
        logger.error(f"Error parsing JSON response: {str(e)}")
        return None

def is_valid_orcid(orcid_id):
    """
    Validates the ORCID ID format.
    """
    pattern = re.compile(r'^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$')
    return bool(pattern.match(orcid_id))

if __name__ == "__main__":
    orcid_id = input("Enter ORCID iD (format: XXXX-XXXX-XXXX-XXXX): ")
    if is_valid_orcid(orcid_id):
        profile = get_orcid_profile(orcid_id)
        save_profile_to_file(profile, "orcid_profile.json")
        print("Profile saved to orcid_profile.json")
    else:
        print("Invalid ORCID iD format.")
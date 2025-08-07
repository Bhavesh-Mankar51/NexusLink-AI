import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Scrapes a LinkedIn profile for information.
    Handles cases where the API does not return person data.
    """
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/Bhavesh-Mankar51/1ff93bacf18e77b4a8f5cb3c8fb97da6/raw/41382364013372f36f5eeffecc4f53bd9ff35ed7/harrison-chase-scrapin.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://api.scrapin.io/v1/enrichment/profile"
        params = {
            "apikey": os.environ.get("SCRAPIN_API_KEY"),
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )

    
    data = response.json().get("person")


    if data:
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", None)
            and k not in ["certifications"]
        }
        return data
    
    return {}

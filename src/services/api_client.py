import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.environ['GOOGLE_SEARCH_API_KEY']
GOOGLE_CSE_ID = os.environ['GOOGLE_SEARCH_CSE_ID']
RAPID_API_KEY = os.environ['RAPID_API_KEY']
RAPID_API_HOST = os.environ['RAPID_API_HOST']


def search_linkedin_profiles(query: str) -> list:
    """Search for LinkedIn profiles using Google Custom Search API"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            links = []
            for item in response.json()['items']:
                links.append(item['link'])
            # Check for next page and fetch up to 2 more pages
            page_count = 1
            while page_count < 3 and 'queries' in response.json() and 'nextPage' in response.json()['queries']:
                next_page = response.json()['queries']['nextPage'][0]
                start_index = next_page['startIndex']
                
                params['start'] = start_index
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    for item in response.json()['items']:
                        links.append(item['link'])
                    page_count += 1
                else:
                    break

            return links
        else:
            print(f"Google Search API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error searching profiles: {e}")
        return []


def get_linkedin_profile(profile_url: str) -> dict:
    """Fetch LinkedIn profile data using RapidAPI"""
    url = "https://fresh-linkedin-profile-data.p.rapidapi.com/get-linkedin-profile"
    params = {
        "linkedin_url": profile_url,
        "include_skills": "false",
        "include_certifications": "false",
        "include_publications": "false",
        "include_honors": "false",
        "include_volunteers": "false",
        "include_projects": "false",
        "include_patents": "false",
        "include_courses": "false",
        "include_organizations": "false",
        "include_profile_status": "false",
        "include_company_public_url": "false"
    }

    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": RAPID_API_HOST
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)    
        if response.status_code == 200:
            return response.json()['data']
        else:
            print(f"LinkedIn API error: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return {} 
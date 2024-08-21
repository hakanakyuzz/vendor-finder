import os
from dotenv import load_dotenv
import requests
from outscraper import ApiClient


load_dotenv()
OUTSCRAPER_API_KEY = os.getenv("OUTSCRAPER_API_KEY")

def get_outscraper_client():
    return ApiClient(api_key=OUTSCRAPER_API_KEY)


def scrape_vendor_data(outscraper_client, final_url):
    try:
        print(f"Scraping data for vendor link: {final_url}")
        results = outscraper_client.emails_and_contacts([final_url])
        print(f"Results for {final_url}: {results}")
        return results
    except Exception as e:
        print(f"Failed to scrape {final_url}: {e}")
        return None


def verify_emails(api_key, emails):
    try:
        url = 'https://api.app.outscraper.com/validators/email'
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json',
        }
        params = {
            'query': emails,
            'async': 'false'
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            result_data = response.json().get('data', [])
            print(f"Verification results: {result_data}")
            return result_data
        else:
            print(f"Failed to verify emails: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error occurred while verifying emails: {e}")
        return []

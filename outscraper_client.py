import os
from dotenv import load_dotenv
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

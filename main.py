from scrapers.woodlands_scraper import scrape_links
from clients.beautifulsoap_client import scrape_vendor_data
from db import connect_to_mongo
from excel import create_excel_file
from website_urls import WEBSITE_URL
from verification import verify_emails
from driver import setup_driver, close_driver
from selenium.common.exceptions import TimeoutException
from utils import (
    get_final_url,
    get_base_url,
    get_base_collection_name,
    insert_vendor_data,
    get_priority_text,
    get_combined_text,
    update_new_collection,
    merge_collections
)


# load_dotenv()
# OUTSCRAPER_API_KEY = os.getenv("OUTSCRAPER_API_KEY")

def main():
    db = connect_to_mongo()
    if db is None:
        return

    driver, wait = setup_driver()
    vendor_links_by_category = scrape_links(driver, wait)

    # outscraper_client = get_outscraper_client()
    processed_urls = set()

    base_collection_name = get_base_collection_name(WEBSITE_URL)
    collection_name = base_collection_name

    valid_links_by_category = {}

    for category, vendor_links in vendor_links_by_category.items():
        collection_name = f"{base_collection_name}_{category.replace(' ', '_')}"
        collection = db[collection_name]
        total_links = len(vendor_links)
        valid_links_by_category[category] = []

        for idx, vendor_link in enumerate(vendor_links):
            print(f"Processing vendor link {idx + 1} of {total_links}")
            final_url = get_final_url(driver, vendor_link)
            if final_url:
                base_url = get_base_url(final_url)
                if base_url in processed_urls:
                    print(f"Skipping duplicate base URL: {base_url}")
                    continue
                processed_urls.add(base_url)

                try:
                    driver.get(final_url)
                except TimeoutException:
                    print(f"Timeout while loading {final_url}, skipping.")
                    continue

                # results = scrape_vendor_data(outscraper_client, base_url)
                results = scrape_vendor_data(base_url)
                if isinstance(results, list):
                    for result in results:
                        if isinstance(result, dict):
                            emails = [email['value'] for email in result.get('emails', [])]

                            # verified_emails = verify_emails(OUTSCRAPER_API_KEY, emails)
                            verified_emails = verify_emails(emails)
                            print(f"Verified emails: {verified_emails}")
                            valid_emails = [email['query'] for email in verified_emails if email.get('status') in ['RECEIVING']]

                            if valid_emails:
                                result['emails'] = [{'value': email} for email in valid_emails]
                                description = result.get('site_data', {}).get('description')

                                driver.get(final_url)
                                combined_text = description
                                if not combined_text:
                                    combined_text = get_priority_text(driver, wait)
                                if not combined_text:
                                    try:
                                        combined_text = get_combined_text(driver, wait)
                                    except Exception as e:
                                        print(f"Error while getting combined text for link: {final_url}. Skipping. Error: {e}")
                                        continue
                                if combined_text:
                                    print(f"Combined text for {final_url}: {combined_text}")
                                    result['combined_text'] = combined_text

                                    insert_vendor_data(collection, category, final_url, result, valid_links_by_category)
                                else:
                                    print(f"No text available for classification for link: {final_url}")
                            else:
                                print(f"No valid emails found for link: {final_url}")
                        else:
                            print(f"Invalid data format for {final_url}: {result}")
                else:
                    print(f"Invalid data format for {final_url}: {results}")
            else:
                print(f"Failed to follow redirect for {vendor_link}")

    close_driver(driver)

    create_excel_file(collection_name)

    update_new_collection(collection_name)

    merge_collections()


if __name__ == "__main__":
    main()
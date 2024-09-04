from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from website_urls import WEBSITE_URL

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    all_links = []

    try:
        # Close the popup by clicking the button with id 'save_cookie_settings_button'
        try:
            print("Closing the popup...")
            close_popup_button = wait.until(EC.element_to_be_clickable((By.ID, 'save_cookie_settings_button')))
            close_popup_button.click()
            time.sleep(2)  # Wait for the popup to close
        except TimeoutException:
            print("Popup did not appear or was not closed in time.")

        while True:
            print("Extracting 'entry_website' links...")
            entry_website_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'entry_website')))
            for div in entry_website_divs:
                try:
                    a_tag = div.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        all_links.append(href)
                        print(f"Extracted link: {href}")
                except NoSuchElementException:
                    print("No a tag found inside entry_website div.")
                    continue

            try:
                print("Handling pagination...")
                next_button = wait.until(EC.element_to_be_clickable((By.ID, 'pagination_next')))
                next_button.click()
                time.sleep(2)  # Wait for the next page to load
            except (TimeoutException, NoSuchElementException):
                print("No more pages found or pagination failed.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Extracted links:")
    for link in all_links:
        print(link)

    return {'category': all_links}

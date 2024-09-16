from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    try:
        close_modal_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mc-closeModal')))
        print("Closing the modal...")
        close_modal_button.click()
        time.sleep(1)
    except (NoSuchElementException, TimeoutException):
        print("No modal found or not clickable, continuing with scraping.")

    collected_listing_links = []
    final_links = []

    while True:
        try:
            print("Collecting listing links from 'directorist-listing-title' h4 elements...")
            h4_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'directorist-listing-title')))

            for h4 in h4_elements:
                try:
                    a_tag = h4.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        collected_listing_links.append(href)
                        print(f"Collected listing link: {href}")
                except NoSuchElementException:
                    print("No 'a' tag found inside 'h4' element.")
                    continue
        except TimeoutException:
            print("No 'directorist-listing-title' h4 elements found.")
            break

        try:
            print("Handling pagination...")
            next_button = driver.find_element(By.CLASS_NAME, 'next')

            if next_button.is_displayed() and next_button.is_enabled():
                print("Clicking the 'Next' page button...")
                next_button.click()
                time.sleep(2)
            else:
                print("Next button is not interactable, stopping pagination.")
                break
        except NoSuchElementException:
            print("No 'Next' button found, stopping pagination.")
            break

    for listing_link in collected_listing_links:
        try:
            print(f"Visiting listing page: {listing_link}")
            driver.get(listing_link)
            time.sleep(2)

            try:
                web_info_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'directorist-single-info-web')))
                value_div = web_info_div.find_element(By.CLASS_NAME, 'directorist-single-info__value')
                a_tag = value_div.find_element(By.TAG_NAME, 'a')
                final_href = a_tag.get_attribute('href')
                if final_href:
                    final_links.append(final_href)
                    print(f"Collected final link: {final_href}")
            except NoSuchElementException:
                print("No 'directorist-single-info-web' or 'directorist-single-info__value' found.")
        except TimeoutException:
            print(f"Failed to load the listing page: {listing_link}")

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

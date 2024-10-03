from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    while True:
        try:
            load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'outlined-button')))
            print("Clicking the 'outlined-button' using JavaScript...")
            time.sleep(3)
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(3)
        except (NoSuchElementException, TimeoutException):
            print("No more 'outlined-button' to click, moving on.")
            break
        except ElementClickInterceptedException:
            print("Button is still being intercepted, retrying.")
            time.sleep(3)

    collected_links = []
    try:
        print("Collecting 'partner-content' links...")
        partner_links = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'partner-content')))
        for a_tag in partner_links:
            href = a_tag.get_attribute('href')
            if href:
                collected_links.append(href)
                print(f"Collected 'partner-content' link: {href}")
    except TimeoutException:
        print("No 'partner-content' links found.")

    final_links = []
    for link in collected_links:
        try:
            print(f"Visiting partner content page: {link}")
            driver.delete_all_cookies()
            driver.get(link)
            time.sleep(2)

            try:
                global_a_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'global')))
                final_href = global_a_tag.get_attribute('href')
                if final_href:
                    final_links.append(final_href)
                    print(f"Collected final link: {final_href}")
            except NoSuchElementException:
                print(f"No 'global' link found on the page {link}.")
        except TimeoutException:
            print(f"Failed to load the partner content page: {link}")

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}
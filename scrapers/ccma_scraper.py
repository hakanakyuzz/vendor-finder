from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import time


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    final_links = []

    while True:
        try:
            print("Collecting links from 'wpbdp-field-association-meta' divs...")
            meta_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'wpbdp-field-association-meta')))

            for meta_div in meta_divs:
                try:
                    value_div = meta_div.find_element(By.CLASS_NAME, 'value')
                    a_tag = value_div.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        final_links.append(href)
                        print(f"Collected link: {href}")
                except NoSuchElementException:
                    print("No 'value' div or 'a' tag found inside 'wpbdp-field-association-meta' div.")
                    continue
        except TimeoutException:
            print("No 'wpbdp-field-association-meta' divs found.")
            break

        try:
            print("Handling pagination...")
            next_span = driver.find_element(By.CLASS_NAME, 'next')
            if next_span:
                print("Clicking the 'Next' page button...")
                next_span.click()
                time.sleep(2)
            else:
                print("No more 'Next' page span found, stopping pagination.")
                break
        except (NoSuchElementException, ElementNotInteractableException):
            print("No 'Next' span tag found or it is not interactable, stopping pagination.")
            break

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}
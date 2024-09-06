from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    all_links = []

    try:
        while True:
            print("Extracting links from 'contact-info' divs...")

            contact_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'contact-info')))
            for div in contact_divs:
                try:
                    p_tags = div.find_elements(By.TAG_NAME, 'p')
                    if len(p_tags) == 2:
                        first_p = p_tags[0]
                        a_tag = first_p.find_element(By.TAG_NAME, 'a')
                        href = a_tag.get_attribute('href')
                        if href:
                            all_links.append(href)
                            print(f"Collected link: {href}")
                    else:
                        print("Skipping div with less than 2 p tags.")
                except NoSuchElementException:
                    print("No a tag found inside the first p tag.")
                    continue

            try:
                print("Handling pagination...")
                a_tags = driver.find_elements(By.TAG_NAME, 'a')
                next_button = None
                for a in a_tags:
                    if 'next' in a.get_attribute('class'):
                        next_button = a
                        break

                if next_button:
                    print("Clicking the 'next' page button...")
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(2)
                else:
                    print("No more 'next' button found, stopping pagination.")
                    break

            except NoSuchElementException:
                print("No 'next' button found, stopping pagination.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Final extracted links:")
    for link in all_links:
        print(link)

    return {'category': all_links}

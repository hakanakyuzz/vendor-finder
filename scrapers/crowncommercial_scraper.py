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
        while True:
            print("Extracting 'govuk-heading-m' links...")
            h3_tags = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'govuk-heading-m')))
            for h3_tag in h3_tags:
                try:
                    a_tag = h3_tag.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        all_links.append(href)
                        print(f"Collected link: {href}")
                except NoSuchElementException:
                    print("No a tag found inside h3 tag with class 'govuk-heading-m'.")
                    continue

            try:
                print("Handling pagination...")
                next_button = driver.find_element(By.XPATH, "//a[@rel='next']")
                if next_button:
                    print("Clicking the next page button...")
                    next_button.click()
                    time.sleep(2)
                else:
                    print("No more pages found.")
                    break
            except NoSuchElementException:
                print("No more pages to paginate.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    final_links = []

    for link in all_links:
        try:
            print(f"Visiting {link}...")
            driver.get(link)

            p_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'break-word')))
            try:
                a_tag = p_tag.find_element(By.TAG_NAME, 'a')
                final_href = a_tag.get_attribute('href')
                if final_href:
                    final_links.append(final_href)
                    print(f"Extracted final link: {final_href}")
            except NoSuchElementException:
                print("No a tag found inside p tag with class 'break-word'.")

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Failed to process link {link}: {e}")
            continue

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}
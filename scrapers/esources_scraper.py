from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    print("Deleting all cookies initially...")
    driver.delete_all_cookies()

    driver.refresh()

    all_links = []

    try:
        while True:
            print("Extracting 'baselinks' links...")
            baselinks_spans = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'baselinks')))
            for span in baselinks_spans:
                try:
                    a_tag = span.find_element(By.CLASS_NAME, 'bold')
                    href = a_tag.get_attribute('href')
                    if href:
                        all_links.append(href)
                        print(f"Extracted link: {href}")
                except NoSuchElementException:
                    print("No a tag found inside baselinks span.")
                    continue

            print("Handling pagination...")
            results_div = wait.until(EC.presence_of_element_located((By.ID, 'results')))
            p_tag = results_div.find_element(By.TAG_NAME, 'p')
            p_children = p_tag.find_elements(By.XPATH, './*')

            last_element = p_children[-1]
            if last_element.tag_name == 'a':
                try:
                    print("Clicking the last 'a' tag to go to the next page...")
                    last_element.click()

                    print("Deleting all cookies after clicking 'Next'...")
                    driver.delete_all_cookies()

                    driver.refresh()
                except TimeoutException:
                    print("Timeout while trying to click the next page link.")
                    break
            elif last_element.tag_name == 'strong':
                print("Reached the last page, pagination is over.")
                break
            else:
                print("Unexpected element type, stopping pagination.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Extracted links:")
    for link in all_links:
        print(link)

    return {'category': all_links}
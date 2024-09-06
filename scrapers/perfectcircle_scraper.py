from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from website_urls import WEBSITE_URL
import time

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    all_links = []

    while True:
        try:
            print("Locating all 'p' tags with 'color--blue-dark' links on the current page...")
            p_tags = driver.find_elements(By.XPATH, "//p//a[contains(@class, 'big')]")
            for a_tag in p_tags:
                href = a_tag.get_attribute('href')
                if href:
                    all_links.append(href)
                    print(f"Extracted link: {href}")

            try:
                print("Attempting to locate and click the 'Next' button...")
                next_buttons = driver.find_elements(By.CSS_SELECTOR, "a.next")
                if next_buttons:
                    next_button = next_buttons[0]
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next")))
                    for _ in range(3):
                        try:
                            next_button.click()
                            break
                        except ElementClickInterceptedException:
                            time.sleep(1)
                            next_buttons = driver.find_elements(By.CSS_SELECTOR, "a.next")
                            if next_buttons:
                                next_button = next_buttons[0]
                            else:
                                break
                    wait.until(EC.staleness_of(next_button))
                    print("Moved to the next page.")
                else:
                    print("No more 'Next' buttons found. Ending pagination.")
                    break

            except (TimeoutException, NoSuchElementException) as e:
                print(f"Failed to find or click 'Next' button: {e}")
                break

        except Exception as e:
            print(f"Error occurred during extraction or pagination: {e}")
            break

    print(f"Found {len(all_links)} links in total")

    return {'category': all_links}

from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    final_links = []
    current_page = 1
    max_page = 104

    while current_page <= max_page:
        print(f"Processing page {current_page}...")

        try:
            print("Collecting 'dd' div links with target='_blank'...")
            dd_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'dd')))

            for div in dd_divs:
                try:
                    a_tag = div.find_element(By.XPATH, ".//a[@target='_blank']")
                    href = a_tag.get_attribute('href')
                    if href:
                        final_links.append(href)
                        print(f"Collected link: {href}")
                except NoSuchElementException:
                    print(f"No 'a' tag with target='_blank' found inside div class 'dd'.")
                    continue

            # Handling pagination
            if current_page < max_page:
                next_page = current_page + 1
                print(f"Looking for the 'Next' page button for page {next_page}...")

                try:
                    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@data-page='{next_page}']")))
                    print(f"Clicking 'Next' button for page {next_page}...")
                    next_button.click()
                    time.sleep(5)  # Giving time for the page to load

                    # Verify the page number changed after clicking "Next"
                    wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'current-page-class'), str(next_page)))
                    current_page += 1

                    # Clean cookies between page loads
                    driver.delete_all_cookies()

                except (TimeoutException, StaleElementReferenceException):
                    print(f"No 'Next' button found for page {next_page} or element is stale. Stopping pagination.")
                    break
                except NoSuchElementException:
                    print(f"No pagination button found for page {next_page}. Stopping pagination.")
                    break
            else:
                print(f"Reached the last page {max_page}.")
                break

        except TimeoutException:
            print(f"Failed to load the page {current_page}, skipping this one.")
            break

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}
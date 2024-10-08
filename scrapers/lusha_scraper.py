from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import random


def scrape_links(driver, wait):
    page_url = WEBSITE_URL
    print(f"Navigating to the website: {page_url}...")
    driver.get(page_url)

    extracted_links = []

    while True:
        all_links = []

        try:
            print("Locating all 'directory-content-box-row' containers...")
            directory_rows = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'directory-content-box-row')))
        except TimeoutException as e:
            print(f"Failed to locate 'directory-content-box-row' containers within the timeout: {e}")
            break

        for row in directory_rows:
            try:
                print("Checking for 'directory-content-box-col' divs inside the row...")
                col_divs = row.find_elements(By.CLASS_NAME, 'directory-content-box-col')
                if not col_divs:
                    print("No 'directory-content-box-col' divs found, skipping this row.")
                    continue

                for col_div in col_divs:
                    try:
                        print("Waiting for anchor tag inside 'directory-content-box-col' to be present...")
                        a_tag = col_div.find_element(By.TAG_NAME, 'a')
                        if a_tag.find_elements(By.TAG_NAME, 'span'):
                            print("Anchor tag contains a span, skipping this column.")
                            continue

                        href = a_tag.get_attribute('href')
                        if href:
                            all_links.append(href)
                    except TimeoutException:
                        print("Anchor tag not found within the timeout, skipping this column.")
                        continue
            except Exception as e:
                print(f"Failed to process a column: {e}")
                continue

        for link in all_links:
            retry_attempts = 3
            while link and retry_attempts > 0:
                try:
                    print(f"Visiting page: {link}")
                    driver.get(link)
                    time.sleep(random.uniform(7, 12))

                    current_url = driver.current_url
                    if current_url != link:
                        print(f"Redirect detected. Expected: {link}, but got: {current_url}")
                        break

                    print("Waiting for 'company-hero-info' div to be present...")
                    hero_info_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'company-hero-info')))

                    print("Waiting for anchor tag inside 'company-hero-info' to be present...")
                    company_link = hero_info_div.find_element(By.TAG_NAME, 'a').get_attribute('href')

                    if company_link:
                        extracted_links.append(company_link)
                        print(f"Extracted link: {company_link}")
                    break

                except TimeoutException as e:
                    print(f"Encountered timeout on page {link}: {e}. Retrying...")
                    retry_attempts -= 1
                    if retry_attempts == 0:
                        print(f"Final attempt failed. Capturing page source for debugging...")
                        page_source_snippet = driver.page_source[:2000]
                        print(f"Page source snippet: {page_source_snippet}")
                        break

                except WebDriverException as e:
                    print(f"WebDriver exception on page {link}: {e}. Breaking out.")
                    break

                except Exception as e:
                    print(f"Failed to process page {link}: {e}")
                    break

        print(f"Returning to the main page: {page_url} to find the Next button...")
        driver.get(page_url)
        time.sleep(random.uniform(7, 12))

        try:
            print("Looking for the 'Next' button to navigate to the next page...")
            next_button_a = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'next')))
            next_page_url = next_button_a.get_attribute('href')

            if next_page_url:
                page_url = next_page_url
                print(f"Navigating directly to the URL: {page_url}")
                driver.get(page_url)

                wait.until(EC.staleness_of(directory_rows[0]))
            else:
                print("No URL found in the 'Next' button. Ending pagination.")
                break
        except TimeoutException:
            print("No 'Next' button found or failed to load next page, ending pagination.")
            break
        except NoSuchElementException:
            print("No 'Next' button available, reached the last page.")
            break
        except Exception as e:
            print(f"Failed to navigate to the next page: {e}")
            break

    print("Extracted links:")
    for link in extracted_links:
        print(link)

    return {'category': extracted_links}
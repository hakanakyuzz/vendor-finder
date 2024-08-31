from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from website_urls import WEBSITE_URL

def scrape_links(driver, wait):
    page_url = WEBSITE_URL
    print(f"Navigating to the website: {page_url}...")
    driver.get(page_url)

    extracted_links = []

    try:
        print("Locating all 'div' elements with class 'col-sm-4'...")
        div_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'col-sm-4')))

        for div_index in range(len(div_elements)):
            attempt = 0
            while attempt < 3:  # Retry up to 3 times in case of stale element
                try:
                    print(f"Processing div element {div_index + 1}/{len(div_elements)} (Attempt {attempt + 1})...")

                    # Re-locate div_elements to avoid stale element reference issues
                    div_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'col-sm-4')))
                    div_element = div_elements[div_index]

                    print("Looking for 'a' tag inside the 'div' element...")
                    a_tag = div_element.find_element(By.TAG_NAME, 'a')

                    href = a_tag.get_attribute('href')
                    if href:
                        print(f"Navigating to the new page: {href}")
                        driver.get(href)

                        try:
                            print("Looking for 'a' tag with class 'tooltip'...")
                            tooltip_link = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tooltip')))

                            final_href = tooltip_link.get_attribute('href')
                            if final_href:
                                extracted_links.append(final_href)
                                print(f"Extracted link: {final_href}")

                        except TimeoutException:
                            print("Tooltip link not found on the new page.")
                        finally:
                            print(f"Returning to the main page: {page_url}")
                            driver.get(page_url)  # Go back to the original page to continue scraping

                    break  # Exit the retry loop if successful

                except (StaleElementReferenceException, NoSuchElementException) as e:
                    print(f"Encountered {e.__class__.__name__} on attempt {attempt + 1}. Retrying...")
                    attempt += 1

    except TimeoutException as e:
        print(f"Failed to locate 'div' elements within the timeout: {e}")

    print("Extracted links:")
    for link in extracted_links:
        print(link)

    return {'category': extracted_links}

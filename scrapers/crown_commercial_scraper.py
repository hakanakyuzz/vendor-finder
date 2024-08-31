from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from website_urls import WEBSITE_URL
import time

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    # Step 1: Collect all the links that lead to other pages of the website
    intermediate_links = []

    while True:
        try:
            print("Locating all 'a' tags inside 'h3' tags...")
            h3_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h3')))
            for h3 in h3_elements:
                try:
                    a_tag = h3.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        intermediate_links.append(href)
                        print(f"Stored intermediate link: {href}")
                except Exception as e:
                    print(f"Failed to process h3 element: {e}")
                    continue
        except TimeoutException:
            print("No h3 elements found on this page.")
            break

        # Handle pagination by clicking the "Next" button
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a[rel='next']")
            time.sleep(5)
            if next_button:
                next_url = next_button.get_attribute('href')
                if next_url:
                    print(f"Found 'next' link: {next_url}")
                    driver.get(next_url)
                    wait.until(EC.staleness_of(h3_elements[0]))  # Wait for the page to load
                else:
                    break
            else:
                break
        except NoSuchElementException:
            print("No 'next' link found, ending pagination.")
            break

    print(f"Collected {len(intermediate_links)} intermediate links. Now visiting each to extract final links.")

    # Step 2: Visit each collected link and extract the final set of links
    final_links = []

    for link in intermediate_links:
        try:
            print(f"Visiting intermediate link: {link}")
            time.sleep(5)
            driver.get(link)
            p_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'break-word')))
            for p in p_elements:
                try:
                    a_tag = p.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        final_links.append(href)
                        print(f"Extracted final link: {href}")
                except Exception as e:
                    print(f"Failed to process p element: {e}")
                    continue
        except Exception as e:
            print(f"Failed to process intermediate link {link}: {e}")
            continue

    print(f"Extracted a total of {len(final_links)} final links.")

    return {'category': final_links}

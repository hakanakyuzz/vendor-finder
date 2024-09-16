from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from website_urls import WEBSITE_URL

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    all_final_links = []

    try:
        print("Collecting links from 'homeCategoryList' divs...")
        category_links = []
        home_category_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'homeCategoryList')))
        for div in home_category_divs:
            try:
                a_tag = div.find_element(By.TAG_NAME, 'a')
                href = a_tag.get_attribute('href')
                if href:
                    category_links.append(href)
                    print(f"Collected category link: {href}")
            except NoSuchElementException:
                print("No a tag found in homeCategoryList div.")
                continue

        for link in category_links:
            print(f"Visiting category link: {link}")
            driver.get(link)
            time.sleep(2)

            while True:
                try:
                    print("Collecting links from 'searchListingCTA' divs...")
                    search_listing_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'searchListingCTA')))
                    for div in search_listing_divs:
                        try:
                            a_tag = div.find_element(By.TAG_NAME, 'a')
                            final_href = a_tag.get_attribute('href')
                            if final_href:
                                all_final_links.append(final_href)
                                print(f"Collected final link: {final_href}")
                        except NoSuchElementException:
                            print("No a tag found in searchListingCTA div.")
                            continue

                    try:
                        next_page_icon = driver.find_element(By.ID, 'nextPage')
                        if 'arrow_active' in next_page_icon.get_attribute('class'):
                            print("Clicking the next page button...")
                            driver.execute_script("arguments[0].click();", next_page_icon)
                            time.sleep(2)
                        else:
                            print("No more active pagination, stopping pagination.")
                            break

                    except NoSuchElementException:
                        print("No 'nextPage' i tag found, stopping pagination.")
                        break

                except TimeoutException:
                    print("Timeout while trying to load 'searchListingCTA' divs.")
                    break

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Final extracted links:")
    for link in all_final_links:
        print(link)

    return {'category': all_final_links}

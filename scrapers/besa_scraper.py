from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from website_urls import WEBSITE_URL
import time

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    initial_links = []
    final_links = []

    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print("Data loading complete, locating 'supplierBlock' a tags...")
        supplier_links = driver.find_elements(By.CLASS_NAME, 'supplierBlock')
        for a_tag in supplier_links:
            try:
                href = a_tag.get_attribute('href')
                if href:
                    initial_links.append(href)
                    print(f"Stored supplier link: {href}")
            except NoSuchElementException:
                print("No href found in supplierBlock a tag.")
                continue

        for link in initial_links:
            try:
                print(f"Navigating to {link}...")
                driver.get(link)

                print("Locating the first 'link' a tag on the page...")
                link_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'link')))
                final_href = link_tag.get_attribute('href')
                if final_href:
                    final_links.append(final_href)
                    print(f"Extracted final link: {final_href}")

            except (TimeoutException, NoSuchElementException) as e:
                print(f"Failed to process link {link}: {e}")
                continue

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

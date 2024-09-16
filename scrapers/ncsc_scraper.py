from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    collected_links = []
    final_links = []

    try:
        print("Collecting links from 'pcf-link' a tags...")
        pcf_links = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pcf-link')))
        for a_tag in pcf_links:
            href = a_tag.get_attribute('href')
            if href:
                collected_links.append(href)
                print(f"Collected link: {href}")
    except TimeoutException:
        print("No 'pcf-link' a tags found.")

    for link in collected_links:
        print(f"Visiting collected link: {link}")
        driver.get(link)
        time.sleep(2)

        try:
            print("Collecting links from 'dd' tags with class 'keyvalue-value'...")
            dd_elements = driver.find_elements(By.CLASS_NAME, 'keyvalue-value')
            time.sleep(2)
            for dd in dd_elements:
                try:
                    p_tag = dd.find_element(By.TAG_NAME, 'p')
                    a_tag = p_tag.find_element(By.TAG_NAME, 'a')
                    final_href = a_tag.get_attribute('href')
                    if final_href and 'mailto' not in final_href:
                        final_links.append(final_href)
                        print(f"Collected final link: {final_href}")
                    else:
                        print("Skipped 'mailto' link.")
                except NoSuchElementException:
                    print("No 'p' or 'a' tag found inside 'dd' tag.")
                    continue

        except Exception as e:
            print(f"Error while collecting links: {e}")
            continue

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

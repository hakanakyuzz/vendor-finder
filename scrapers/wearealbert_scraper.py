from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    final_links = []

    try:
        print("Collecting 'supplier__detail--website' links...")
        li_tags = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'supplier__detail--website')))

        for li in li_tags:
            try:
                a_tag = li.find_element(By.TAG_NAME, 'a')
                href = a_tag.get_attribute('href')
                if href:
                    final_links.append(href)
                    print(f"Collected link: {href}")
            except NoSuchElementException:
                print("No 'a' tag found inside 'supplier__detail--website'.")
                continue

    except TimeoutException:
        print("No 'supplier__detail--website' elements found.")

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

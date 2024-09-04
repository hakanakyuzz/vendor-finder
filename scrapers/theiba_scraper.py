from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from website_urls import WEBSITE_URL


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    all_links = []

    try:
        print("Locating 'lbox' divs...")
        lbox_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lbox')))
        for div in lbox_divs:
            try:
                a_tag = div.find_element(By.TAG_NAME, 'a')
                href = a_tag.get_attribute('href')
                if href:
                    all_links.append(href)
                    print(f"Extracted link: {href}")
            except NoSuchElementException:
                print("No a tag found inside lbox div.")
                continue

    except TimeoutException:
        print("Timed out waiting for lbox divs to load.")

    print("Extracted links:")
    for link in all_links:
        print(link)

    return {'category': all_links}

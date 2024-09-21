from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    final_links = []

    try:
        print("Collecting 'card__link' a tags...")
        a_tags = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'card__link')))

        for a_tag in a_tags:
            try:
                href = a_tag.get_attribute('href')
                if href:
                    final_links.append(href)
                    print(f"Collected link: {href}")
            except NoSuchElementException:
                print("No 'href' found inside 'card__link' a tag.")
                continue
    except TimeoutException:
        print("No 'card__link' elements found on the page.")

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

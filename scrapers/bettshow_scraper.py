from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
from website_urls import WEBSITE_URL

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    collected_links = []
    final_links = []

    try:
        print("Looking for the cookie consent button...")
        cookie_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        cookie_button.click()
        print("Cookie consent button clicked.")
        time.sleep(2)
    except TimeoutException:
        print("Cookie consent button not found or already clicked.")

    while True:
        try:
            print("Collecting links from the current page...")
            exhibitor_links = wait.until(EC.presence_of_all_elements_located((
                By.CLASS_NAME, 'm-exhibitors-list__items__item__header__title__link')))

            for a_tag in exhibitor_links:
                href = a_tag.get_attribute('href')
                if href:
                    collected_links.append(href)
                    print(f"Collected link: {href}")

            try:
                print("Handling pagination...")
                next_button = driver.find_element(By.CLASS_NAME, 'pagination__list__item__link--next')
                if next_button:
                    print("Clicking the 'Next' page button...")
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(2)
                else:
                    print("No more 'Next' page button found, stopping pagination.")
                    break
            except StaleElementReferenceException:
                print("Stale element reference encountered, retrying...")
                time.sleep(1)

        except NoSuchElementException:
            print("No 'Next' button found or no more pages, stopping.")
            break

    for link in collected_links:
        print(f"Visiting collected link: {link}")
        driver.get(link)
        time.sleep(2)

        try:
            print("Collecting final links from 'p-button--primary' a tags...")
            final_a_tags = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'p-button--primary')))
            for a_tag in final_a_tags:
                final_href = a_tag.get_attribute('href')
                if final_href:
                    final_links.append(final_href)
                    print(f"Collected final link: {final_href}")

        except NoSuchElementException:
            print("No 'p-button--primary' a tag found.")
            continue

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

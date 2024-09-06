from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from website_urls import WEBSITE_URL


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    all_links = []

    while True:
        try:
            print("Locating h2 tags with class 'h2--thin' to extract links...")
            h2_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'h2--thin')))
            for h2 in h2_elements:
                try:
                    a_tag = h2.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        all_links.append(href)
                        print(f"Stored link: {href}")
                except NoSuchElementException:
                    print("No a tag found inside h2 element.")
                    continue
        except TimeoutException:
            print("No more h2 tags with class 'h2--thin' found, ending pagination.")
            break

        try:
            print("Looking for the 'Next' button to go to the next page...")
            next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pager__item--next')))
            next_button.click()
            wait.until(EC.staleness_of(h2_elements[0]))
        except (TimeoutException, NoSuchElementException):
            print("No 'Next' button found or no more pages, stopping pagination.")
            break

    print(f"Collected {len(all_links)} links to visit for final extraction.")

    extracted_links = []
    for link in all_links:
        try:
            print(f"Visiting page: {link}")
            driver.get(link)
            company_contact_p = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'company-contact')))
            a_tag = company_contact_p.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            if href:
                extracted_links.append(href)
                print(f"Extracted link: {href}")
        except Exception as e:
            print(f"Failed to process page {link}: {e}")
            continue

    print("Extracted links:")
    for link in extracted_links:
        print(link)

    return {'category': extracted_links}

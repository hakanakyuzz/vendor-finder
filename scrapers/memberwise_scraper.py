from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    final_links = []

    try:
        print("Collecting 'wpbdp-field-type-url' div links...")
        url_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'wpbdp-field-type-url')))

        for div in url_divs:
            try:
                inner_div = div.find_element(By.TAG_NAME, 'div')
                a_tag = inner_div.find_element(By.TAG_NAME, 'a')
                href = a_tag.get_attribute('href')
                if href:
                    final_links.append(href)
                    print(f"Collected link: {href}")
            except NoSuchElementException:
                print("No 'a' tag found inside 'wpbdp-field-type-url' div.")
                continue
    except TimeoutException:
        print("No 'wpbdp-field-type-url' elements found on the page.")

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

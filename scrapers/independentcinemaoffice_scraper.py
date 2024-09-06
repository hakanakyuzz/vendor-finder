from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from website_urls import WEBSITE_URL

def scrape_links(driver, wait):
    page_url = WEBSITE_URL
    print(f"Navigating to the website: {page_url}...")
    driver.get(page_url)

    extracted_links = []

    try:
        print("Checking for the cookie consent button...")
        cookie_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-cookie-agree')))
        cookie_button.click()
        print("Cookie consent button clicked.")
    except TimeoutException:
        print("Cookie consent button not found or already handled.")

    # Step 2: Scrape initial `a` tags
    def scrape_a_tags():
        print("Looking for `a` tags with `target='_blank'` and no child elements...")
        a_tags = driver.find_elements(By.XPATH, "//a[@target='_blank' and not(*)]")

        for a_tag in a_tags:
            href = a_tag.get_attribute('href')
            if href:
                extracted_links.append(href)
                print(f"Extracted link: {href}")

    scrape_a_tags()

    try:
        print("Locating `ul` element with class 'distributors-filter'...")
        ul_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'distributors-filter')))
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

        for li_index in range(len(li_elements)):
            attempt = 0
            while attempt < 3:
                try:
                    print(f"Processing li element {li_index + 1}/{len(li_elements)} (Attempt {attempt + 1})...")

                    ul_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'distributors-filter')))
                    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
                    li_element = li_elements[li_index]

                    print("Looking for 'a' tag inside the 'li' element...")
                    a_tag = li_element.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        print(f"Navigating to the new page: {href}")
                        driver.get(href)
                        scrape_a_tags()
                        print(f"Returning to the main page: {page_url}")
                        driver.get(page_url)
                    break
                except (StaleElementReferenceException, NoSuchElementException) as e:
                    print(f"Encountered {e.__class__.__name__} on attempt {attempt + 1}. Retrying...")
                    attempt += 1

    except TimeoutException as e:
        print(f"Failed to locate `ul` element with class 'distributors-filter' within the timeout: {e}")

    print("Extracted links:")
    for link in extracted_links:
        print(link)

    return {'category': extracted_links}

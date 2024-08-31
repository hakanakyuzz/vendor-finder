from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from website_urls import WEBSITE_URL

def scrape_links(driver, wait):
    page_url = WEBSITE_URL
    print(f"Navigating to the website: {page_url}...")
    driver.get(page_url)

    extracted_links = []

    try:
        print("Locating the `div` with class 'entry-content' and itemprop='text'...")
        entry_content_div = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.entry-content[itemprop="text"]')
        ))

        print("Finding all `<p>` tags inside the `entry-content` div...")
        p_tags = entry_content_div.find_elements(By.TAG_NAME, 'p')

        print("Filtering `<p>` tags with no child elements...")
        for p_tag in p_tags:
            # Check if the p tag has no children
            if not p_tag.find_elements(By.XPATH, './*'):
                link_text = p_tag.text.strip()  # Extract the text and remove any surrounding whitespace
                if link_text:
                    extracted_links.append(link_text)
                    print(f"Extracted link text: {link_text}")

    except TimeoutException as e:
        print(f"Failed to locate `div` or `<p>` elements within the timeout: {e}")

    print("Extracted links:")
    for link in extracted_links:
        print(link)

    return {'category': extracted_links}
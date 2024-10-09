from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from website_urls import WEBSITE_URL


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    initial_links = []
    final_links = []

    try:
        print("Locating 'cta' a tags...")
        cta_links = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cta')))
        for cta in cta_links:
            try:
                href = cta.get_attribute('href')
                if href:
                    initial_links.append(href)
                    print(f"Stored initial link: {href}")
            except NoSuchElementException:
                print("No href found in cta a tag.")
                continue

        for link in initial_links:
            try:
                print(f"Navigating to {link}...")
                driver.get(link)

                print("Locating the 'pure-u-12-24' divs in the page...")
                pure_u_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pure-u-12-24')))

                for div in pure_u_divs:
                    p_tags = div.find_elements(By.TAG_NAME, 'p')
                    for p_tag in p_tags:
                        a_tags = p_tag.find_elements(By.TAG_NAME, 'a')
                        for a_tag in a_tags:
                            href = a_tag.get_attribute('href')
                            if href:
                                final_links.append(href)
                                print(f"Extracted final link: {href}")
            except (TimeoutException, NoSuchElementException) as e:
                print(f"Failed to process link {link}: {e}")
                continue

    except TimeoutException:
        print("Timed out waiting for cta a tags to load.")

    print("Extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}
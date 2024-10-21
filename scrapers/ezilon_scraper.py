from selenium.webdriver.common.by import By


def scrape_links(driver, wait):
    def explore_page(url, visited_links, extracted_links):
        try:
            print(f"Navigating to {url}...")
            driver.get(url)
            visited_links.add(url)

            ul_elements = driver.find_elements(By.TAG_NAME, 'ul')
            for ul in ul_elements:
                li_elements = ul.find_elements(By.TAG_NAME, 'li')
                for li in li_elements:
                    a_tag = li.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')

                    if href:
                        if a_tag.get_attribute('class') == 'title':
                            if href not in extracted_links:
                                extracted_links.append(href)
                                print(f"Extracted link: {href}")
                        else:
                            if href not in visited_links:
                                links_to_visit.append(href)

        except Exception as e:
            print(f"Error navigating to {url}: {e}")

    print("Starting scraping process...")
    base_url = "https://uk.ezilon.com/"
    visited_links = set()
    extracted_links = []
    links_to_visit = [base_url]

    while links_to_visit:
        current_link = links_to_visit.pop(0)
        if current_link not in visited_links:
            explore_page(current_link, visited_links, extracted_links)

    print(f"Finished scraping. Extracted {len(extracted_links)} links.")
    return {'category': extracted_links}
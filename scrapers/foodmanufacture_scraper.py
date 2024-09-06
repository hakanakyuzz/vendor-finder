from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    pagination_links = []
    all_links = []

    try:
        print("Collecting the first 23 'PaginationAlpha-item' links...")
        pagination_items = driver.find_elements(By.CLASS_NAME, 'PaginationAlpha-item')
        for index, pagination_item in enumerate(pagination_items[:23]):
            try:
                href = pagination_item.get_attribute('href')
                if href:
                    pagination_links.append(href)
                    print(f"Collected pagination link {index + 1}: {href}")
            except NoSuchElementException:
                print(f"No href found in pagination item {index + 1}")
                continue

        for page_index, pagination_link in enumerate(pagination_links):
            try:
                print(f"Visiting pagination link {page_index + 1}: {pagination_link}")
                driver.get(pagination_link)

                print("Extracting 'Teaser-title' links...")
                teaser_titles = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Teaser-title')))
                for teaser in teaser_titles:
                    try:
                        a_tag = teaser.find_element(By.TAG_NAME, 'a')
                        href = a_tag.get_attribute('href')
                        if href:
                            all_links.append(href)
                            print(f"Collected link: {href}")
                    except NoSuchElementException:
                        print("No a tag found inside h3 tag with class 'Teaser-title'.")
                        continue

            except TimeoutException:
                print(f"Timeout while trying to visit pagination link {page_index + 1}")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    final_links = []

    for link in all_links:
        try:
            print(f"Visiting {link}...")
            driver.get(link)

            ezurl_fields = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ezurl-field')))
            if ezurl_fields:
                final_href = ezurl_fields[0].get_attribute('href')
                if final_href:
                    final_links.append(final_href)
                    print(f"Extracted ezurl link: {final_href}")
            else:
                print("No ezurl-field links found on the page.")

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Failed to process link {link}: {e}")
            continue

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

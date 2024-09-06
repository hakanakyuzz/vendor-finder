from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from website_urls import WEBSITE_URL


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    all_links = []
    click_counter = 0

    try:
        while True:
            print("Extracting 'sd-loop-supplier' links...")
            articles = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sd-loop-supplier')))
            for article in articles:
                try:
                    a_tag = article.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        all_links.append(href)
                        print(f"Collected link: {href}")
                except NoSuchElementException:
                    print("No a tag found inside article tag with class 'sd-loop-supplier'.")
                    continue

            try:
                print("Handling pagination...")
                ul_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pagination__items--end')))
                li_tag = ul_tag.find_element(By.TAG_NAME, 'li')
                next_page_link = li_tag.find_element(By.TAG_NAME, 'a')
                if next_page_link:
                    print(f"Clicking the next page button (Click count: {click_counter + 1})...")
                    next_page_link.click()
                    time.sleep(2)
                    click_counter += 1
                else:
                    print("No more pages found.")
                    break
            except NoSuchElementException:
                print("No more pages to paginate.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    final_links = []

    for link in all_links:
        try:
            print(f"Visiting {link}...")
            driver.get(link)

            div_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sd-supplier-online-links')))
            ul_tag = div_tag.find_element(By.TAG_NAME, 'ul')
            li_tag = ul_tag.find_element(By.TAG_NAME, 'li')
            a_tag = li_tag.find_element(By.TAG_NAME, 'a')
            final_href = a_tag.get_attribute('href')
            if final_href:
                final_links.append(final_href)
                print(f"Extracted final link: {final_href}")

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Failed to process link {link}: {e}")
            continue

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

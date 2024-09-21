from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    final_links = []
    footer_links = []

    # while True:
    #     try:
    #         print("Clicking 'pager__item' to load more pages...")
    #         pager_item = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pager__item')))
    #         pager_item.click()
    #     except (NoSuchElementException, TimeoutException):
    #         print("No more 'pager__item' elements to click, stopping pagination.")
    #         break

    try:
        print("Collecting 'o-tile__footer' links...")
        footers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'o-tile__footer')))
        for footer in footers:
            try:
                a_tag = footer.find_element(By.TAG_NAME, 'a')
                href = a_tag.get_attribute('href')
                if href:
                    footer_links.append(href)
                    print(f"Collected footer link: {href}")
            except NoSuchElementException:
                print("No 'a' tag found in 'o-tile__footer'.")
                continue
    except TimeoutException:
        print("No 'o-tile__footer' elements found.")

    for footer_link in footer_links:
        try:
            print(f"Visiting footer link: {footer_link}")
            driver.get(footer_link)

            print("Collecting 'o-list__item' > 'span' > 'a' links...")
            list_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'o-list__item')))
            for li_tag in list_items:
                try:
                    span_tag = li_tag.find_element(By.TAG_NAME, 'span')
                    a_tag = span_tag.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        final_links.append(href)
                        print(f"Collected final link: {href}")
                except NoSuchElementException:
                    print("No 'a' tag found inside 'span' in 'o-list__item'.")
                    continue
        except TimeoutException:
            print(f"Failed to load the page for {footer_link}, skipping this one.")

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

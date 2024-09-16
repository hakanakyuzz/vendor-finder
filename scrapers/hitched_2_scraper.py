from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    final_links = []
    category_links = []
    vendor_tile_links = []

    try:
        cookie_close_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        print("Closing the cookie consent modal...")
        cookie_close_button.click()
    except TimeoutException:
        print("No cookie consent modal found, continuing.")

    try:
        category_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.app-searcher-category-input')))
        category_input.click()
    except ElementClickInterceptedException as e:
        print(f"Failed to click the category input: {e}")
        return

    try:
        # print("Collecting 'searcherCategoriesDropdownSublist__item' links...")
        # category_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'searcherCategoriesDropdownSublist__item')))
        print("Collecting 'searcherCategoriesDropdownList__item ' links...")
        category_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'searcherCategoriesDropdownList__item ')))
        for li_tag in category_items:
            try:
                a_tag = li_tag.find_element(By.TAG_NAME, 'a')
                href = a_tag.get_attribute('href')
                if href:
                    category_links.append(href)
                    print(f"Collected category link: {href}")
            except NoSuchElementException:
                print("No 'a' tag found inside 'searcherCategoriesDropdownSublist__item'.")
                continue
    except TimeoutException:
        print("No 'searcherCategoriesDropdownSublist__item' found.")

    for category_link in category_links:
        try:
            print(f"Visiting category page: {category_link}")
            driver.get(category_link)

            while True:
                try:
                    print("Collecting 'vendorTile__title' links...")
                    vendor_links = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'vendorTile__title')))
                    for a_tag in vendor_links:
                        href = a_tag.get_attribute('href')
                        if href:
                            vendor_tile_links.append(href)
                            print(f"Collected vendor tile link: {href}")

                    print("Handling pagination...")
                    pagination_next_span = driver.find_elements(By.CLASS_NAME, 'pagination__next')
                    if pagination_next_span:
                        try:
                            next_button = pagination_next_span[0].find_element(By.TAG_NAME, 'button')
                            if next_button.is_enabled():
                                print("Clicking the 'Next' page button...")
                                driver.execute_script("arguments[0].click();", next_button)
                                driver.delete_all_cookies()
                            else:
                                print("Next button is not enabled, stopping pagination.")
                                break
                        except NoSuchElementException:
                            print("No 'Next' button found inside 'pagination__next'.")
                            break
                    else:
                        print("No 'pagination__next' found, stopping pagination.")
                        break

                except TimeoutException:
                    print("No 'vendorTile__title' links found on this page, moving on.")
                    break

        except TimeoutException:
            print(f"Failed to load the category page: {category_link}, skipping this one.")

    for vendor_link in vendor_tile_links:
        try:
            print(f"Visiting vendor page: {vendor_link}")
            driver.get(vendor_link)

            if driver.find_elements(By.CLASS_NAME, 'storefrontHeadingWebsite__label.app-storefront-visit-website'):
                try:
                    print("Collecting final website link...")
                    website_span = wait.until(EC.presence_of_element_located(
                        (By.CLASS_NAME, 'storefrontHeadingWebsite__label.app-storefront-visit-website')))
                    final_href = website_span.get_attribute('data-href')
                    if final_href:
                        final_links.append(final_href)
                        print(f"Collected final link: {final_href}")
                except NoSuchElementException:
                    print(f"No 'storefrontHeadingWebsite__label' found on the vendor page {vendor_link}.")
            else:
                print(f"No website span found on the vendor page {vendor_link}, skipping.")
        except TimeoutException:
            print(f"Failed to load the vendor page: {vendor_link}, skipping this one.")

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

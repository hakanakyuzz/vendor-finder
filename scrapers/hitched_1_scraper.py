from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    final_links = []
    venue_city_links = []
    vendor_tile_links = []

    try:
        print("Collecting 'venuesCitiesList__link' links...")
        city_links = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'venuesCitiesList__link')))
        for a_tag in city_links:
            href = a_tag.get_attribute('href')
            if href:
                venue_city_links.append(href)
                print(f"Collected venue city link: {href}")
    except TimeoutException:
        print("No 'venuesCitiesList__link' found.")

    for city_link in venue_city_links:
        try:
            print(f"Visiting city page: {city_link}")
            driver.get(city_link)

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
            print(f"Failed to load the city page: {city_link}, skipping this one.")

    for vendor_link in vendor_tile_links:
        try:
            print(f"Visiting vendor page: {vendor_link}")
            driver.get(vendor_link)

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
        except TimeoutException:
            print(f"Failed to load the vendor page: {vendor_link}, skipping this one.")

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

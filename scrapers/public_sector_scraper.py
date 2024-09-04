from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from website_urls import WEBSITE_URL
import time

def scrape_links(driver, wait):

    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    all_links = []

    for region_value in range(1, 13):
        try:
            driver.get(WEBSITE_URL)
            print(f"Selecting region with value: {region_value}")
            select_region = wait.until(EC.presence_of_element_located((By.ID, 'idRegion')))
            time.sleep(2)
            select_region.find_element(By.XPATH, f"./option[@value='{region_value}']").click()

            print("Clicking the submit button...")
            submit_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn')))
            time.sleep(2)
            submit_button.click()

            while True:
                try:
                    print("Locating supplier divs...")
                    supplier_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'supplier')))
                    for supplier_div in supplier_divs:
                        try:
                            a_tag = supplier_div.find_element(By.TAG_NAME, 'a')
                            href = a_tag.get_attribute('href')
                            if href:
                                all_links.append(href)
                                print(f"Extracted link: {href}")
                        except NoSuchElementException:
                            print("No a tag found inside supplier div.")
                            continue

                    print("Handling pagination...")
                    pagination_ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pagination')))
                    active_li = pagination_ul.find_element(By.XPATH, ".//li[@class='active']")
                    try:
                        next_li = active_li.find_element(By.XPATH, "following-sibling::li[1]")
                        if next_li:
                            wait.until(EC.element_to_be_clickable(next_li))
                            time.sleep(2)
                            next_li.click()
                            wait.until(EC.staleness_of(supplier_divs[0]))
                        else:
                            print("No next page found, breaking pagination loop.")
                            break
                    except NoSuchElementException:
                        print("No next page available, finishing pagination.")
                        break

                except (TimeoutException, NoSuchElementException) as e:
                    print(f"Pagination failed or no more pages: {e}")
                    break

        except Exception as e:
            print(f"Failed to process region {region_value}: {e}")
            continue

    print("Extracted links:")
    for link in all_links:
        print(link)

    return {'category': all_links}

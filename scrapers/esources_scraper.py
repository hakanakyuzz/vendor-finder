from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    print("Deleting all cookies initially...")
    driver.delete_all_cookies()

    driver.refresh()

    all_links = []

    try:
        while True:
            print("Extracting 'baselinks' links...")
            baselinks_spans = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'baselinks')))
            for span in baselinks_spans:
                try:
                    a_tag = span.find_element(By.CLASS_NAME, 'bold')
                    href = a_tag.get_attribute('href')
                    if href:
                        all_links.append(href)
                        print(f"Extracted link: {href}")
                except NoSuchElementException:
                    print("No a tag found inside baselinks span.")
                    continue

            print("Handling pagination...")
            results_div = wait.until(EC.presence_of_element_located((By.ID, 'results')))
            p_tag = results_div.find_element(By.TAG_NAME, 'p')
            p_children = p_tag.find_elements(By.XPATH, './*')

            last_element = p_children[-1]
            if last_element.tag_name == 'a':
                try:
                    print("Clicking the last 'a' tag to go to the next page...")
                    last_element.click()

                    print("Deleting all cookies after clicking 'Next'...")
                    driver.delete_all_cookies()

                    driver.refresh()
                except TimeoutException:
                    print("Timeout while trying to click the next page link.")
                    break
            elif last_element.tag_name == 'strong':
                print("Reached the last page, pagination is over.")
                break
            else:
                print("Unexpected element type, stopping pagination.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Extracted links:")
    for link in all_links:
        print(link)

    return {'category': all_links}


#################


# from website_urls import WEBSITE_URL
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
#
# def scrape_links(driver, wait):
#     print("Navigating to the website...")
#     driver.get(WEBSITE_URL)
#
#     all_links = []
#
#     try:
#         print("Locating the main 'home-left' container...")
#         home_left_div = wait.until(EC.presence_of_element_located((By.ID, 'home-left')))
#     except Exception as e:
#         print(f"Failed to locate 'home-left' container: {e}")
#         return {'category': []}
#
#     for list_class in ['left-list', 'right-list']:
#         try:
#             print(f"Locating the '{list_class}' ul element...")
#             ul_element = home_left_div.find_element(By.CLASS_NAME, list_class)
#             li_elements = ul_element.find_elements(By.XPATH, './li[strong]')
#         except Exception as e:
#             print(f"Failed to locate '{list_class}' ul element: {e}")
#             continue
#
#         for li in li_elements:
#             try:
#                 strong_tag = li.find_element(By.TAG_NAME, 'strong')
#                 a_tag = strong_tag.find_element(By.TAG_NAME, 'a')
#                 href = a_tag.get_attribute('href')
#                 if href:
#                     all_links.append(href)
#             except Exception as e:
#                 print(f"Failed to process an li element: {li.text} with error {e}")
#                 continue
#
#     print(f"Found {len(all_links)} links in total")
#
#     extracted_links = []
#     for link in all_links:
#         while link:
#             try:
#                 print(f"Visiting page: {link}")
#                 driver.get(link)
#                 spread_maincol_div = wait.until(EC.presence_of_element_located((By.ID, 'spread-maincol')))
#
#                 row_divs = spread_maincol_div.find_elements(By.XPATH, ".//div[contains(@class, 'clearfix')]")
#
#                 stop_pagination = False
#
#                 for row_div in row_divs:
#                     try:
#                         logo_collapse_div = row_div.find_element(By.XPATH, ".//div[contains(@class, 'logo-collapse') or contains(@class, 'logo-collapsed')]")
#                         if 'logo-collapsed' in logo_collapse_div.get_attribute('class'):
#                             print("Found logo-collapsed div, stopping further processing on this page and pagination.")
#                             stop_pagination = True
#                             break
#                         baselinks_span = logo_collapse_div.find_element(By.CLASS_NAME, 'baselinks')
#                         bold_a = baselinks_span.find_element(By.CLASS_NAME, 'bold')
#                         href = bold_a.get_attribute('href')
#                         if href:
#                             extracted_links.append(href)
#                             print(f"Extracted link: {href}")
#                     except Exception as e:
#                         print(f"Failed to process a row div: {e}")
#                         continue
#
#                 if stop_pagination:
#                     break
#
#                 print(f"Extracted {len(extracted_links)} links from the current page")
#
#                 try:
#                     results_div = wait.until(EC.presence_of_element_located((By.ID, 'results')))
#                     next_button = results_div.find_element(By.XPATH, ".//p[1]//a[text()='Next»']")
#                     if next_button:
#                         next_button.click()
#                         wait.until(EC.staleness_of(spread_maincol_div))
#                         link = driver.current_url
#                         print(f"Next page link found: {link}")
#                     else:
#                         link = None
#                 except (TimeoutException, NoSuchElementException):
#                     print("No more pages found")
#                     link = None
#
#             except Exception as e:
#                 print(f"Failed to process page {link}: {e}")
#                 break
#
#     print("Extracted links:")
#     for link in extracted_links:
#         print(link)
#
#     return {'category': extracted_links}
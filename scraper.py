from config import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


# WEBSITE_URL = "https://www.lusha.com/company-search/wholesale/30/united-kingdom/12/"

import time
import random

def scrape_links(driver, wait):
    page_url = WEBSITE_URL
    print(f"Navigating to the website: {page_url}...")
    driver.get(page_url)

    extracted_links = []

    while True:
        all_links = []

        try:
            print("Locating all 'directory-content-box-row' containers...")
            directory_rows = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'directory-content-box-row')))
        except TimeoutException as e:
            print(f"Failed to locate 'directory-content-box-row' containers within the timeout: {e}")
            break

        for row in directory_rows:
            try:
                print("Checking for 'directory-content-box-col' divs inside the row...")
                col_divs = row.find_elements(By.CLASS_NAME, 'directory-content-box-col')
                if not col_divs:
                    print("No 'directory-content-box-col' divs found, skipping this row.")
                    continue

                for col_div in col_divs:
                    try:
                        print("Waiting for anchor tag inside 'directory-content-box-col' to be present...")
                        a_tag = col_div.find_element(By.TAG_NAME, 'a')
                        if a_tag.find_elements(By.TAG_NAME, 'span'):
                            print("Anchor tag contains a span, skipping this column.")
                            continue

                        href = a_tag.get_attribute('href')
                        if href:
                            all_links.append(href)
                    except TimeoutException:
                        print("Anchor tag not found within the timeout, skipping this column.")
                        continue
            except Exception as e:
                print(f"Failed to process a column: {e}")
                continue

        for link in all_links:
            retry_attempts = 3
            while link and retry_attempts > 0:
                try:
                    print(f"Visiting page: {link}")
                    driver.get(link)
                    time.sleep(random.uniform(7, 12))  # Random delay between 2 to 5 seconds

                    current_url = driver.current_url
                    if current_url != link:
                        print(f"Redirect detected. Expected: {link}, but got: {current_url}")
                        break

                    print("Waiting for 'company-hero-info' div to be present...")
                    hero_info_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'company-hero-info')))

                    print("Waiting for anchor tag inside 'company-hero-info' to be present...")
                    company_link = hero_info_div.find_element(By.TAG_NAME, 'a').get_attribute('href')

                    if company_link:
                        extracted_links.append(company_link)
                        print(f"Extracted link: {company_link}")
                    break

                except TimeoutException as e:
                    print(f"Encountered timeout on page {link}: {e}. Retrying...")
                    retry_attempts -= 1
                    if retry_attempts == 0:
                        print(f"Final attempt failed. Capturing page source for debugging...")
                        page_source_snippet = driver.page_source[:2000]
                        print(f"Page source snippet: {page_source_snippet}")
                        break

                except WebDriverException as e:
                    print(f"WebDriver exception on page {link}: {e}. Breaking out.")
                    break

                except Exception as e:
                    print(f"Failed to process page {link}: {e}")
                    break

        print(f"Returning to the main page: {page_url} to find the Next button...")
        driver.get(page_url)
        time.sleep(random.uniform(7, 12))  # Random delay before looking for the Next button

        try:
            print("Looking for the 'Next' button to navigate to the next page...")
            next_button_a = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'next')))
            next_page_url = next_button_a.get_attribute('href')

            if next_page_url:
                page_url = next_page_url  # Update the page_url with the next page URL
                print(f"Navigating directly to the URL: {page_url}")
                driver.get(page_url)

                wait.until(EC.staleness_of(directory_rows[0]))
            else:
                print("No URL found in the 'Next' button. Ending pagination.")
                break
        except TimeoutException:
            print("No 'Next' button found or failed to load next page, ending pagination.")
            break
        except NoSuchElementException:
            print("No 'Next' button available, reached the last page.")
            break
        except Exception as e:
            print(f"Failed to navigate to the next page: {e}")
            break

    print("Extracted links:")
    for link in extracted_links:
        print(link)

    return {'category': extracted_links}



#####################################################


# def scrape_links(driver, wait):
#     print("Navigating to the website...")
#     driver.get(WEBSITE_URL)
#
#     extracted_links = []
#
#     while True:
#         all_links = []
#         goBack = 0
#
#         try:
#             print("Locating all 'directory-content-box-row' containers...")
#             directory_rows = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'directory-content-box-row')))
#         except TimeoutException as e:
#             print(f"Failed to locate 'directory-content-box-row' containers within the timeout: {e}")
#             break
#
#         for row in directory_rows:
#             try:
#                 print("Checking for 'directory-content-box-col' divs inside the row...")
#                 col_divs = row.find_elements(By.CLASS_NAME, 'directory-content-box-col')
#                 if not col_divs:
#                     print("No 'directory-content-box-col' divs found, skipping this row.")
#                     continue
#
#                 for col_div in col_divs:
#                     try:
#                         print("Waiting for anchor tag inside 'directory-content-box-col' to be present...")
#                         a_tag = col_div.find_element(By.TAG_NAME, 'a')
#                         if a_tag.find_elements(By.TAG_NAME, 'span'):
#                             print("Anchor tag contains a span, skipping this column.")
#                             continue
#
#                         href = a_tag.get_attribute('href')
#                         if href:
#                             all_links.append(href)
#                     except TimeoutException:
#                         print("Anchor tag not found within the timeout, skipping this column.")
#                         continue
#             except Exception as e:
#                 print(f"Failed to process a column: {e}")
#                 continue
#
#         for link in all_links:
#             retry_attempts = 3
#             while link and retry_attempts > 0:
#                 try:
#                     print(f"Visiting page: {link}")
#                     driver.get(link)
#
#                     current_url = driver.current_url
#                     if current_url != link:
#                         print(f"Redirect detected. Expected: {link}, but got: {current_url}")
#                         break
#
#                     print("Waiting for 'company-hero-info' div to be present...")
#                     hero_info_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'company-hero-info')))
#
#                     print("Waiting for anchor tag inside 'company-hero-info' to be present...")
#                     company_link = hero_info_div.find_element(By.TAG_NAME, 'a').get_attribute('href')
#
#                     if company_link:
#                         extracted_links.append(company_link)
#                         print(f"Extracted link: {company_link}")
#                         goBack+=1
#                     break
#
#                 except TimeoutException as e:
#                     print(f"Encountered timeout on page {link}: {e}. Retrying...")
#                     retry_attempts -= 1
#                     if retry_attempts == 0:
#                         print(f"Final attempt failed. Capturing page source for debugging...")
#                         page_source_snippet = driver.page_source[:2000]
#                         print(f"Page source snippet: {page_source_snippet}")
#                         break
#
#                 except WebDriverException as e:
#                     print(f"WebDriver exception on page {link}: {e}. Breaking out.")
#                     break
#
#                 except Exception as e:
#                     print(f"Failed to process page {link}: {e}")
#                     break
#
#         while True:
#             try:
#                 print("Looking for the 'Next' button to navigate to the next page...")
#                 next_button_a = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'next')))
#                 print("Next button found. Ready to navigate to the next page.")
#                 break
#             except TimeoutException:
#                 print("No 'Next' button found on the current page, going back one page...")
#                 driver.execute_script("window.history.go(-1)")
#
#             except Exception as e:
#                 print(f"Failed to go back or find the 'Next' button: {e}")
#                 break
#
#         try:
#             next_page_url = next_button_a.get_attribute('href')
#
#             if next_page_url:
#                 print(f"Navigating directly to the URL: {next_page_url}")
#                 driver.get(next_page_url)
#
#                 wait.until(EC.staleness_of(directory_rows[0]))
#             else:
#                 print("No URL found in the 'Next' button. Ending pagination.")
#                 break
#         except TimeoutException:
#             print("No 'Next' button found or failed to load next page, ending pagination.")
#             break
#         except NoSuchElementException:
#             print("No 'Next' button available, reached the last page.")
#             break
#         except Exception as e:
#             print(f"Failed to navigate to the next page: {e}")
#             break
#
#     print("Extracted links:")
#     for link in extracted_links:
#         print(link)
#
#     return {'category': extracted_links}


#############


# WEBSITE_URL = "https://www.bheta.co.uk/supplier-search/"

# def scrape_links(driver, wait):
#     print("Navigating to the website...")
#     driver.get(WEBSITE_URL)
#
#     all_links = []
#
#     try:
#         print("Locating the main 'content-wrapper' container...")
#         content_wrapper = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'content-wrapper')))
#     except Exception as e:
#         print(f"Failed to locate 'content-wrapper' container: {e}")
#         return {'category': []}
#
#     def process_page():
#         try:
#             print("Locating the second 'row' div...")
#             row_divs = content_wrapper.find_elements(By.CLASS_NAME, 'row')
#             if len(row_divs) < 2:
#                 print("Less than two 'row' divs found")
#                 return False
#
#             second_row_div = row_divs[1]
#             col_md_4_divs = second_row_div.find_elements(By.CLASS_NAME, 'col-md-4')
#
#             for col_div in col_md_4_divs:
#                 try:
#                     crm_result_div = col_div.find_element(By.CLASS_NAME, 'crm-result')
#                     a_tag = crm_result_div.find_element(By.TAG_NAME, 'a')
#                     link = a_tag.get_attribute('href')
#                     if link:
#                         print(f"Found link: {link}")
#                         all_links.append(link)
#                 except Exception as e:
#                     print(f"Failed to process 'col-md-4' div: {e}")
#                     continue
#
#         except Exception as e:
#             print(f"Error processing page: {e}")
#             return False
#
#         return True
#
#     def visit_page(link):
#         try:
#             driver.get(link)
#             p_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'crm_search_member_detail_website')))
#             a_tag = p_tag.find_element(By.TAG_NAME, 'a')
#             final_link = a_tag.get_attribute('href')
#             if final_link:
#                 print(f"Extracted final link: {final_link}")
#                 return final_link
#         except Exception as e:
#             print(f"Failed to extract link from new page: {e}")
#             return None
#
#     def click_next_button():
#         try:
#             print("Looking for the next button...")
#             next_button = wait.until(
#                 EC.element_to_be_clickable(
#                     (By.CLASS_NAME, 'btn.crm_search_pagination_button.crm_search_pagination_next')
#                 )
#             )
#             print(f"Next button found: {next_button.text}")
#
#             next_button.click()
#             return True
#         except TimeoutException:
#             print("Next button not found: TimeoutException")
#             return False
#         except NoSuchElementException:
#             print("Next button not found: NoSuchElementException")
#             return False
#         except Exception as e:
#             print(f"Error clicking next button: {e}")
#             return False
#
#     while True:
#         if not process_page():
#             break
#
#         if not click_next_button():
#             break
#
#         try:
#             wait.until(EC.staleness_of(content_wrapper))
#             content_wrapper = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'content-wrapper')))
#         except Exception as e:
#             print(f"Error waiting for new content wrapper: {e}")
#             break
#
#     final_links = []
#     for link in all_links:
#         final_link = visit_page(link)
#         if final_link:
#             final_links.append(final_link)
#
#     print(f"Extracted {len(final_links)} final links:")
#     for link in final_links:
#         print(link)
#
#     return {'category': final_links}


#############


# WEBSITE_URL = "https://www.confex.ltd.uk/suppliers_list.asp"

# def scrape_links(driver, wait):
#     print("Navigating to the website...")
#     driver.get(WEBSITE_URL)
#
#     all_links = []
#
#     try:
#         print("Locating the main 'tbody' container...")
#         tbody_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
#     except Exception as e:
#         print(f"Failed to locate 'tbody' container: {e}")
#         return {'category': []}
#
#     try:
#         print("Locating all 'tr' elements inside the 'tbody' container...")
#         tr_elements = tbody_element.find_elements(By.TAG_NAME, 'tr')
#     except Exception as e:
#         print(f"Failed to locate 'tr' elements: {e}")
#         return {'category': []}
#
#     for tr in tr_elements:
#         try:
#             td_elements = tr.find_elements(By.TAG_NAME, 'td')
#             if len(td_elements) < 3:
#                 continue
#
#             second_td = td_elements[1]
#             a_tag = second_td.find_element(By.TAG_NAME, 'a')
#             href = a_tag.get_attribute('href')
#             if href:
#                 all_links.append(href)
#         except Exception as e:
#             print(f"Failed to process a tr element: {tr.text} with error {e}")
#             continue
#
#     print(f"Found {len(all_links)} links in total")
#
#     print("Extracted links:")
#     for link in all_links:
#         print(link)
#
#     return {'category': all_links}


#############


# WEBSITE_URL = "https://www.esources.co.uk/suppliers.php"

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


#############


# WEBSITE_URL = "https://www.great.gov.uk/international/trade/search/?q=&industries=CLOTHING_FOOTWEAR_AND_FASHION&industries=CREATIVE_AND_MEDIA&industries=FOOD_AND_DRINK&industries=GIFTWARE_JEWELLERY_AND_TABLEWARE&industries=HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS&industries=RETAIL_AND_LUXURY&industries=TEXTILES_INTERIOR_TEXTILES_AND_CARPETS"

# def scrape_links(driver, wait):
#     print("Navigating to the website...")
#     driver.get(WEBSITE_URL)
#
#     # links_by_category = {}
#     # links_by_category['category'] = []
#     links_by_category = {'category': []}  # Assuming a single category for simplicity
#
#     while True:
#         print("Locating the main category container...")
#         parent_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'column-two-thirds-l')))
#
#         print("Locating the list of links...")
#         ul_element = parent_div.find_element(By.TAG_NAME, 'ul')
#         li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
#
#         for li in li_elements:
#             a_tag = li.find_element(By.TAG_NAME, 'a')
#             href = a_tag.get_attribute('href')
#             if href:
#                 links_by_category['category'].append(href)
#         print(f"Found {len(links_by_category['category'])} links in the main category")
#
#         try:
#             paginator_div = parent_div.find_element(By.ID, 'paginator')
#             next_button = paginator_div.find_element(By.ID, 'paginator-next')
#             if next_button:
#                 next_button.click()
#                 wait.until(EC.staleness_of(parent_div))  # Wait until the page is reloaded
#             else:
#                 break  # No next button, exit the loop
#         except Exception as e:
#             print(f"No paginator found or failed to click next: {e}")
#             break  # Exit the loop if paginator is not found or click fails
#
#     vendor_links_by_category = {}
#     for category, links in links_by_category.items():
#         print(f"Processing category page links for {category}...")
#         vendor_links_by_category[category] = []
#         for link in links:
#             print(f"Visiting category page: {link}")
#             driver.get(link)
#             try:
#                 wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ellipsis')))
#                 dd_elements = driver.find_elements(By.CLASS_NAME, 'ellipsis')
#                 for dd_element in dd_elements:
#                     a_tag = dd_element.find_element(By.TAG_NAME, 'a')
#                     vendor_href = a_tag.get_attribute('href')
#                     if vendor_href:
#                         vendor_links_by_category[category].append(vendor_href)
#             except Exception as e:
#                 print(f"Failed to process {link}: {e}")
#         print(f"Found {len(vendor_links_by_category[category])} vendor links.")
#     return vendor_links_by_category


#############


# WEBSITE_URL = "https://www.thewholesaler.co.uk/"

# def scrape_links(driver, wait):
#     print("Navigating to the website...")
#     driver.get(WEBSITE_URL)
#
#     print("Locating the main category container...")
#     parent_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gb-grid-wrapper-e30b329c')))
#     sub_div_classes = [
#         'gb-grid-column-d16cc483',
#         # 'gb-grid-column-e5fcc923',
#         # 'gb-grid-column-213f0e2d',
#         # 'gb-grid-column-f8ae52c9'
#     ]
#
#     links_by_category = {}
#     for sub_div_class in sub_div_classes:
#         print(f"Processing sub-div: {sub_div_class}")
#         sub_div = parent_div.find_element(By.CLASS_NAME, sub_div_class)
#         container_div = sub_div.find_element(By.CLASS_NAME, f'gb-container-{sub_div_class.split("-")[-1]}')
#         inside_container_div = container_div.find_element(By.CLASS_NAME, 'gb-inside-container')
#         ul_element = inside_container_div.find_element(By.CLASS_NAME, 'wp-block-list')
#
#         category_name = sub_div_class.split('-')[-1]
#         links_by_category[category_name] = []
#
#         li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
#         for li in li_elements[:1]:
#             a_tag = li.find_element(By.TAG_NAME, 'a')
#             href = a_tag.get_attribute('href')
#             if href:
#                 links_by_category[category_name].append(href)
#         print(f"Found {len(links_by_category[category_name])} links in category {category_name}")
#
#     vendor_links_by_category = {}
#     for category, links in links_by_category.items():
#         print(f"Processing category page links for {category}...")
#         vendor_links_by_category[category] = []
#         for link in links:
#             print(f"Visiting category page: {link}")
#             driver.get(link)
#             try:
#                 wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'button.purple.small.round')))
#                 anchor_elements = driver.find_elements(By.CLASS_NAME, 'button.purple.small.round')
#                 for anchor_element in anchor_elements:
#                     vendor_href = anchor_element.get_attribute('href')
#                     if vendor_href:
#                         vendor_links_by_category[category].append(vendor_href)
#                 print(f"Found {len(vendor_links_by_category[category])} vendor links on {link}")
#             except Exception as e:
#                 print(f"Failed to process {link}: {e}")
#     return vendor_links_by_category


#############

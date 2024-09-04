# old function for WEBSITE_URL = "https://www.lusha.com/company-search/wholesale/30/united-kingdom/12/"

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


##############


# The webpage that I got banned. This is a scraper function for that webpage

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from website_urls import WEBSITE_URL
# import time
#
# def scrape_links(driver, wait):
#     print("Navigating to the website...")
#     driver.get(WEBSITE_URL)
#
#     # Step 1: Collect all the links that lead to other pages of the website
#     intermediate_links = []
#
#     while True:
#         try:
#             print("Locating all 'a' tags inside 'h3' tags...")
#             h3_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h3')))
#             for h3 in h3_elements:
#                 try:
#                     a_tag = h3.find_element(By.TAG_NAME, 'a')
#                     href = a_tag.get_attribute('href')
#                     if href:
#                         intermediate_links.append(href)
#                         print(f"Stored intermediate link: {href}")
#                 except Exception as e:
#                     print(f"Failed to process h3 element: {e}")
#                     continue
#         except TimeoutException:
#             print("No h3 elements found on this page.")
#             break
#
#         # Handle pagination by clicking the "Next" button
#         try:
#             next_button = driver.find_element(By.CSS_SELECTOR, "a[rel='next']")
#             time.sleep(5)
#             if next_button:
#                 next_url = next_button.get_attribute('href')
#                 if next_url:
#                     print(f"Found 'next' link: {next_url}")
#                     driver.get(next_url)
#                     wait.until(EC.staleness_of(h3_elements[0]))  # Wait for the page to load
#                 else:
#                     break
#             else:
#                 break
#         except NoSuchElementException:
#             print("No 'next' link found, ending pagination.")
#             break
#
#     print(f"Collected {len(intermediate_links)} intermediate links. Now visiting each to extract final links.")
#
#     # Step 2: Visit each collected link and extract the final set of links
#     final_links = []
#
#     for link in intermediate_links:
#         try:
#             print(f"Visiting intermediate link: {link}")
#             time.sleep(5)
#             driver.get(link)
#             p_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'break-word')))
#             for p in p_elements:
#                 try:
#                     a_tag = p.find_element(By.TAG_NAME, 'a')
#                     href = a_tag.get_attribute('href')
#                     if href:
#                         final_links.append(href)
#                         print(f"Extracted final link: {href}")
#                 except Exception as e:
#                     print(f"Failed to process p element: {e}")
#                     continue
#         except Exception as e:
#             print(f"Failed to process intermediate link {link}: {e}")
#             continue
#
#     print(f"Extracted a total of {len(final_links)} final links.")
#
#     return {'category': final_links}


##############



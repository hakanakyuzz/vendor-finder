from config import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    all_links = []

    try:
        print("Locating the main 'content-wrapper' container...")
        content_wrapper = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'content-wrapper')))
    except Exception as e:
        print(f"Failed to locate 'content-wrapper' container: {e}")
        return {'category': []}

    def process_page():
        try:
            print("Locating the second 'row' div...")
            row_divs = content_wrapper.find_elements(By.CLASS_NAME, 'row')
            if len(row_divs) < 2:
                print("Less than two 'row' divs found")
                return False

            second_row_div = row_divs[1]
            col_md_4_divs = second_row_div.find_elements(By.CLASS_NAME, 'col-md-4')

            for col_div in col_md_4_divs:
                try:
                    crm_result_div = col_div.find_element(By.CLASS_NAME, 'crm-result')
                    a_tag = crm_result_div.find_element(By.TAG_NAME, 'a')
                    link = a_tag.get_attribute('href')
                    if link:
                        print(f"Found link: {link}")
                        all_links.append(link)
                except Exception as e:
                    print(f"Failed to process 'col-md-4' div: {e}")
                    continue

        except Exception as e:
            print(f"Error processing page: {e}")
            return False

        return True

    def visit_page(link):
        try:
            driver.get(link)
            p_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'crm_search_member_detail_website')))
            a_tag = p_tag.find_element(By.TAG_NAME, 'a')
            final_link = a_tag.get_attribute('href')
            if final_link:
                print(f"Extracted final link: {final_link}")
                return final_link
        except Exception as e:
            print(f"Failed to extract link from new page: {e}")
            return None

    def click_next_button():
        try:
            print("Looking for the next button...")
            next_button = wait.until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'btn.crm_search_pagination_button.crm_search_pagination_next')
                )
            )
            print(f"Next button found: {next_button.text}")

            next_button.click()
            return True
        except TimeoutException:
            print("Next button not found: TimeoutException")
            return False
        except NoSuchElementException:
            print("Next button not found: NoSuchElementException")
            return False
        except Exception as e:
            print(f"Error clicking next button: {e}")
            return False

    while True:
        if not process_page():
            break

        if not click_next_button():
            break

        try:
            wait.until(EC.staleness_of(content_wrapper))
            content_wrapper = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'content-wrapper')))
        except Exception as e:
            print(f"Error waiting for new content wrapper: {e}")
            break

    final_links = []
    for link in all_links:
        final_link = visit_page(link)
        if final_link:
            final_links.append(final_link)

    print(f"Extracted {len(final_links)} final links:")
    for link in final_links:
        print(link)

    return {'category': final_links}
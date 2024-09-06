from selenium.common.exceptions import TimeoutException, NoSuchElementException
from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_links(driver, wait):
    page_url = WEBSITE_URL
    print(f"Navigating to the website: {page_url}...")
    driver.get(page_url)

    extracted_links = []
    popup_closed = False

    def close_popup_if_present():
        nonlocal popup_closed
        if not popup_closed:
            try:
                print("Checking for the presence of the ESC popup button...")

                esc_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.backdrop-close"))
                )

                esc_button.click()
                popup_closed = True
                print("Popup closed.")
            except TimeoutException:
                print("ESC popup button not found or popup already closed.")
                popup_closed = True

    close_popup_if_present()

    load_more_clicks = 0
    max_clicks = 862

    while load_more_clicks < max_clicks:
        try:
            print(f"Attempt {load_more_clicks + 1} to click the 'Load More' button...")
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'sp-backdrop-info')))

            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'StylableButton2545352419__label')))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)

            close_popup_if_present()

            load_more_clicks += 1

        except (TimeoutException, NoSuchElementException):
            print("Button no longer exists or could not be found.")
            break
        except Exception as e:
            print(f"Error occurred while clicking the button: {e}")
            break

    try:
        print("Locating all relevant 'p' elements with classes 'font_8 wixui-rich-text__text'...")
        p_elements = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'p.font_8.wixui-rich-text__text')))

        for p_element in p_elements:
            try:
                print("Looking for 'span' elements inside the 'p' element...")
                span_elements = p_element.find_elements(By.CLASS_NAME, 'wixui-rich-text__text')

                for span_element in span_elements:
                    print("Looking for 'a' tags with 'data-auto-recognition' attribute inside 'span'...")
                    a_tags = span_element.find_elements(By.XPATH, ".//a[@data-auto-recognition='true']")

                    for a_tag in a_tags:
                        href = a_tag.get_attribute('href')
                        if href:
                            extracted_links.append(href)
                            print(f"Extracted link: {href}")

            except Exception as e:
                print(f"Failed to process a 'p' element: {e}")
                continue

    except TimeoutException as e:
        print(f"Failed to locate 'p' elements within the timeout: {e}")

    print("Extracted links:")
    for link in extracted_links:
        print(link)

    return {'category': extracted_links}

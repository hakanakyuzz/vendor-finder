from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    try:
        close_cookie_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cookie_action_close_header')))
        print("Clicking the cookie close button...")
        close_cookie_button.click()
    except (NoSuchElementException, TimeoutException):
        print("No cookie close button found or it's not clickable, continuing with scraping.")

    collected_profile_links = []

    try:
        print("Finding and clicking 'dropdown-item' elements...")
        dropdown_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'dropdown-item')))
        for item in dropdown_items:
            try:
                print(f"Clicking dropdown item: {item.text}")

                driver.execute_script("arguments[0].scrollIntoView(true);", item)
                driver.execute_script("arguments[0].click();", item)

                while True:
                    try:
                        load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more-suppliers')))
                        print("Clicking the 'load-more-suppliers' button...")
                        driver.execute_script("arguments[0].click();", load_more_button)
                    except (NoSuchElementException, TimeoutException):
                        print("No more 'load-more-suppliers' button, moving on.")
                        break

                try:
                    print("Collecting profile links...")
                    profile_links = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'font-weight-bold')))
                    for a_tag in profile_links:
                        profile_href = a_tag.get_attribute('href')
                        if profile_href:
                            collected_profile_links.append(profile_href)
                            print(f"Collected profile link: {profile_href}")
                except TimeoutException:
                    print("No profile links found after clicking dropdown item.")

            except ElementClickInterceptedException:
                print(f"Failed to click dropdown item: {item.text}, moving to the next one.")
            except NoSuchElementException:
                print(f"Failed to interact with dropdown item: {item.text}.")
    except TimeoutException:
        print("No 'dropdown-item' elements found.")

    final_links = []
    for profile_link in collected_profile_links:
        try:
            print(f"Visiting profile page: {profile_link}")
            driver.get(profile_link)

            try:
                btn_large_a_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-large')))
                final_href = btn_large_a_tag.get_attribute('href')
                if final_href:
                    final_links.append(final_href)
                    print(f"Collected final link: {final_href}")
            except NoSuchElementException:
                print(f"No 'btn-large' link found on the profile page {profile_link}.")

        except TimeoutException:
            print(f"Failed to load the profile page: {profile_link}, skipping this one.")
        except Exception as e:
            print(f"Error occurred while processing {profile_link}: {e}, skipping this one.")

    final_links.extend(collected_profile_links)

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

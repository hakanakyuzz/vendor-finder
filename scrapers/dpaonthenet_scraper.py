from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    initial_links = []
    final_links = []

    try:
        print("Locating 'cvText' td tags and collecting first 103 a tags...")
        cvText_tds = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cvText')))

        count = 0
        for td in cvText_tds:
            if count >= 103:
                break
            try:
                a_tags = td.find_elements(By.TAG_NAME, 'a')
                for a_tag in a_tags:
                    if count >= 103:
                        break
                    href = a_tag.get_attribute('href')
                    if href:
                        initial_links.append(href)
                        print(f"Stored initial link: {href}")
                        count += 1
            except NoSuchElementException:
                print("No a tag found in cvText td.")
                continue

        for link in initial_links:
            try:
                print(f"Navigating to {link}...")
                driver.get(link)

                print("Locating the 5th tr element on the page...")
                tr_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))

                if len(tr_elements) >= 5:
                    target_tr = tr_elements[4]
                    td_elements = target_tr.find_elements(By.TAG_NAME, 'td')

                    if len(td_elements) >= 2:
                        target_td = td_elements[1]
                        try:
                            a_tag = target_td.find_element(By.TAG_NAME, 'a')
                            final_href = a_tag.get_attribute('href')
                            if final_href:
                                final_links.append(final_href)
                                print(f"Extracted final link: {final_href}")
                        except NoSuchElementException:
                            text_link = target_td.text.strip()
                            if text_link.startswith("Web:"):
                                text_link = text_link.replace("Web:", "").strip()

                            if text_link and not (text_link.startswith("http://") or text_link.startswith("https://")):
                                if text_link.startswith("www."):
                                    text_link = "http://" + text_link
                                else:
                                    text_link = "http://" + text_link

                            if text_link:
                                final_links.append(text_link)
                                print(f"Processed text link: {text_link}")

            except (TimeoutException, NoSuchElementException) as e:
                print(f"Failed to process link {link}: {e}")
                continue

    except TimeoutException:
        print("Timed out waiting for cvText td tags to load.")

    print("Extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

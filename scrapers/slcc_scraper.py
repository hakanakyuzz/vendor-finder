from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    all_links = []

    try:
        while True:
            print("Extracting links from 'inner' divs...")

            divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'inner')))
            for div in divs:
                try:
                    p_tags = div.find_elements(By.TAG_NAME, 'p')
                    if p_tags:
                        last_p = p_tags[-1]
                        a_tag = last_p.find_element(By.TAG_NAME, 'a')
                        href = a_tag.get_attribute('href')
                        if href:
                            all_links.append(href)
                            print(f"Collected link: {href}")
                    else:
                        print("No p tags found in this div.")
                except NoSuchElementException:
                    print("No a tag found inside the last p tag.")
                    continue

            try:
                print("Handling pagination...")

                ul_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'plant_page_numbers')))

                li_tags = ul_tag.find_elements(By.TAG_NAME, 'li')

                if li_tags:
                    last_li = li_tags[-1]

                    try:
                        a_tag = last_li.find_element(By.TAG_NAME, 'a')
                        if a_tag:
                            print("Clicking the last 'a' tag to go to the next page...")
                            driver.execute_script("arguments[0].scrollIntoView(true);", a_tag)
                            time.sleep(1)

                            driver.execute_script("arguments[0].click();", a_tag)
                            time.sleep(2)
                        else:
                            print("No more pages, stopping pagination.")
                            break

                    except NoSuchElementException:
                        print("No 'a' tag found in the last 'li', stopping pagination.")
                        break
                else:
                    print("No 'li' tags found, stopping pagination.")
                    break

            except NoSuchElementException:
                print("No pagination found, stopping.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Final extracted links:")
    for link in all_links:
        print(link)

    return {'category': all_links}

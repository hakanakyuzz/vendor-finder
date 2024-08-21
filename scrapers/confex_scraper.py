from config import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    all_links = []

    try:
        print("Locating the main 'tbody' container...")
        tbody_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
    except Exception as e:
        print(f"Failed to locate 'tbody' container: {e}")
        return {'category': []}

    try:
        print("Locating all 'tr' elements inside the 'tbody' container...")
        tr_elements = tbody_element.find_elements(By.TAG_NAME, 'tr')
    except Exception as e:
        print(f"Failed to locate 'tr' elements: {e}")
        return {'category': []}

    for tr in tr_elements:
        try:
            td_elements = tr.find_elements(By.TAG_NAME, 'td')
            if len(td_elements) < 3:
                continue

            second_td = td_elements[1]
            a_tag = second_td.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            if href:
                all_links.append(href)
        except Exception as e:
            print(f"Failed to process a tr element: {tr.text} with error {e}")
            continue

    print(f"Found {len(all_links)} links in total")

    print("Extracted links:")
    for link in all_links:
        print(link)

    return {'category': all_links}
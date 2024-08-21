from config import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    # links_by_category = {}
    # links_by_category['category'] = []
    links_by_category = {'category': []}

    while True:
        print("Locating the main category container...")
        parent_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'column-two-thirds-l')))

        print("Locating the list of links...")
        ul_element = parent_div.find_element(By.TAG_NAME, 'ul')
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

        for li in li_elements:
            a_tag = li.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            if href:
                links_by_category['category'].append(href)
        print(f"Found {len(links_by_category['category'])} links in the main category")

        try:
            paginator_div = parent_div.find_element(By.ID, 'paginator')
            next_button = paginator_div.find_element(By.ID, 'paginator-next')
            if next_button:
                next_button.click()
                wait.until(EC.staleness_of(parent_div))
            else:
                break
        except Exception as e:
            print(f"No paginator found or failed to click next: {e}")
            break

    vendor_links_by_category = {}
    for category, links in links_by_category.items():
        print(f"Processing category page links for {category}...")
        vendor_links_by_category[category] = []
        for link in links:
            print(f"Visiting category page: {link}")
            driver.get(link)
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ellipsis')))
                dd_elements = driver.find_elements(By.CLASS_NAME, 'ellipsis')
                for dd_element in dd_elements:
                    a_tag = dd_element.find_element(By.TAG_NAME, 'a')
                    vendor_href = a_tag.get_attribute('href')
                    if vendor_href:
                        vendor_links_by_category[category].append(vendor_href)
            except Exception as e:
                print(f"Failed to process {link}: {e}")
        print(f"Found {len(vendor_links_by_category[category])} vendor links.")
    return vendor_links_by_category
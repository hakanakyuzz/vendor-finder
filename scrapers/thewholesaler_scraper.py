from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    print("Locating the main category container...")
    parent_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gb-grid-wrapper-e30b329c')))
    sub_div_classes = [
        'gb-grid-column-d16cc483',
        'gb-grid-column-e5fcc923',
        'gb-grid-column-213f0e2d',
        'gb-grid-column-f8ae52c9'
    ]

    all_vendor_links = []
    for sub_div_class in sub_div_classes:
        print(f"Processing sub-div: {sub_div_class}")
        sub_div = parent_div.find_element(By.CLASS_NAME, sub_div_class)
        container_div = sub_div.find_element(By.CLASS_NAME, f'gb-container-{sub_div_class.split("-")[-1]}')
        inside_container_div = container_div.find_element(By.CLASS_NAME, 'gb-inside-container')
        ul_element = inside_container_div.find_element(By.CLASS_NAME, 'wp-block-list')

        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        for li in li_elements:
            a_tag = li.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            if href:
                all_vendor_links.append(href)
        print(f"Found {len(all_vendor_links)} total links so far")

    vendor_links_by_category = {
        'all_vendors': []
    }

    for link in all_vendor_links:
        print(f"Visiting category page: {link}")
        driver.get(link)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'button.purple.small.round')))
            anchor_elements = driver.find_elements(By.CLASS_NAME, 'button.purple.small.round')
            for anchor_element in anchor_elements:
                vendor_href = anchor_element.get_attribute('href')
                if vendor_href:
                    vendor_links_by_category['all_vendors'].append(vendor_href)
            print(f"Found {len(vendor_links_by_category['all_vendors'])} total vendor links so far")
        except Exception as e:
            print(f"Failed to process {link}: {e}")

    return vendor_links_by_category

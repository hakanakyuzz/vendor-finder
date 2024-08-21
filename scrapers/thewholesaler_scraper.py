from config import WEBSITE_URL
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

    links_by_category = {}
    for sub_div_class in sub_div_classes:
        print(f"Processing sub-div: {sub_div_class}")
        sub_div = parent_div.find_element(By.CLASS_NAME, sub_div_class)
        container_div = sub_div.find_element(By.CLASS_NAME, f'gb-container-{sub_div_class.split("-")[-1]}')
        inside_container_div = container_div.find_element(By.CLASS_NAME, 'gb-inside-container')
        ul_element = inside_container_div.find_element(By.CLASS_NAME, 'wp-block-list')

        category_name = sub_div_class.split('-')[-1]
        links_by_category[category_name] = []

        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        for li in li_elements:
            a_tag = li.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            if href:
                links_by_category[category_name].append(href)
        print(f"Found {len(links_by_category[category_name])} links in category {category_name}")

    vendor_links_by_category = {}
    for category, links in links_by_category.items():
        print(f"Processing category page links for {category}...")
        vendor_links_by_category[category] = []
        for link in links:
            print(f"Visiting category page: {link}")
            driver.get(link)
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'button.purple.small.round')))
                anchor_elements = driver.find_elements(By.CLASS_NAME, 'button.purple.small.round')
                for anchor_element in anchor_elements:
                    vendor_href = anchor_element.get_attribute('href')
                    if vendor_href:
                        vendor_links_by_category[category].append(vendor_href)
                print(f"Found {len(vendor_links_by_category[category])} vendor links on {link}")
            except Exception as e:
                print(f"Failed to process {link}: {e}")
    return vendor_links_by_category
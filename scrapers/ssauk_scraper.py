from website_urls import WEBSITE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def scrape_links(driver, wait):
    print("Navigating to the website...")
    driver.get(WEBSITE_URL)

    collected_links = []
    final_links = []

    try:
        print("Collecting 'article-img' div links...")
        article_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'article-img')))

        for div in article_divs:
            try:
                a_tag = div.find_element(By.TAG_NAME, 'a')
                href = a_tag.get_attribute('href')
                if href:
                    collected_links.append(href)
                    print(f"Collected article link: {href}")
            except NoSuchElementException:
                print("No 'a' tag found inside 'article-img' div.")
                continue
    except TimeoutException:
        print("No 'article-img' elements found on the page.")

    for link in collected_links:
        try:
            print(f"Visiting article page: {link}")
            driver.get(link)

            try:
                print("Looking for 'a' tag with target='_blank'...")
                a_tag = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@target='_blank']")))
                final_href = a_tag.get_attribute('href')
                if final_href:
                    final_links.append(final_href)
                    print(f"Collected final link: {final_href}")
            except NoSuchElementException:
                print(f"No 'a' tag with target='_blank' found on the article page {link}.")
        except TimeoutException:
            print(f"Failed to load the article page: {link}, skipping this one.")

    print("Final extracted links:")
    for link in final_links:
        print(link)

    return {'category': final_links}

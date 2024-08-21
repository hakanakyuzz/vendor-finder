from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from transformers import pipeline
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import categories
import random
import re


def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A5341f Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait


def get_final_url(driver, initial_url):
    try:
        driver.get(initial_url)
        final_url = driver.current_url
        if final_url.startswith("http"):
            return final_url
        else:
            print(f"Invalid final URL: {final_url}")
            return None
    except Exception as e:
        print(f"Error getting final URL for {initial_url}: {e}")
        return None


def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def get_base_collection_name(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.netloc.replace('www.', '').replace('.', '_')}"
    return base_url


def classify_text(text, categories):
    print("Initializing pipeline...")
    pipe = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli", device=-1)
    print("Pipeline initialized.")

    print("Running classification...")
    result = pipe(text, candidate_labels=categories)
    print("Classification completed.")

    print("Result:", result)

    if not result['scores']:
        print("No confident classification result.")
        return "No confident classification result.", None

    max_score_index = result['scores'].index(max(result['scores']))
    best_category = result['labels'][max_score_index]
    best_score = result['scores'][max_score_index]
    print(text)

    if best_score < 0.4:
        print("No confident classification result.")
        return "No confident classification result.", None

    print(f"Best category: {best_category}, with score: {best_score}")

    return best_category, best_score


def get_combined_text(driver, wait):
    body_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    page_html = body_element.get_attribute('innerHTML')
    soup = BeautifulSoup(page_html, 'html.parser')

    texts = []

    title_tag = soup.find('title')
    if title_tag:
        texts.append(title_tag.get_text())

    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        texts.append(meta_description.get('content'))

    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords:
        texts.append(meta_keywords.get('content'))

    for element in ['h1', 'h2', 'h3', 'p', 'li']:
        for tag in soup.find_all(element):
            texts.append(tag.get_text())

    combined_text = ' '.join(texts)
    words = combined_text.split()

    limited_text = ' '.join(words[:60])

    return limited_text


def get_priority_text(driver, wait):
    try:
        meta_description = wait.until(EC.presence_of_element_located((By.XPATH, "//meta[@name='description']")))
        content = meta_description.get_attribute("content")
        words = content.split()
        limited_text = ' '.join(words[:60])
        return limited_text
    except:
        return None


def calculate_weight(doc):
    filled_fields = 0
    classification = doc.get('classification', {})

    if classification.get('category', ''):
        filled_fields += 14
    # if classification.get('subcategory', ''):
        # filled_fields += 7
    if doc.get('query'):
        filled_fields += 10
    if doc.get('emails', [{'value': ''}])[0]['value']:
        filled_fields += 10
    if doc.get('phones', [{'value': ''}])[0]['value']:
        filled_fields += 10
    if doc.get('details', {}).get('country', ''):
        filled_fields += 17
    if doc.get('details', {}).get('city', ''):
        filled_fields += 10
    if doc.get('socials', {}).get('instagram', ''):
        filled_fields += 4.4
    if doc.get('socials', {}).get('facebook', ''):
        filled_fields += 4.4
    if doc.get('socials', {}).get('twitter', ''):
        filled_fields += 4.4
    if doc.get('socials', {}).get('youtube', ''):
        filled_fields += 4.4
    if doc.get('socials', {}).get('linkedin', ''):
        filled_fields += 4.4
    if doc.get('site_data', {}).get('description', ''):
        filled_fields += 7

    return filled_fields


def close_driver(driver):
    driver.quit()
    print("Data scraping, storage, and classification completed successfully.")


def verify_emails(emails):
    priority_patterns = {
        'high': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
        'medium': re.compile(r'^(?!.*(info|support|contact)).*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
        'low': re.compile(r'^(info|support|contact)@.*'),
    }

    verified_emails = []

    for email in emails:
        if priority_patterns['high'].match(email):
            print(f"High priority email: {email}")
            verified_emails.append({'query': email, 'status': 'RECEIVING', 'priority': 'high'})
        elif priority_patterns['medium'].match(email):
            print(f"Medium priority email: {email}")
            verified_emails.append({'query': email, 'status': 'RECEIVING', 'priority': 'medium'})
        elif priority_patterns['low'].match(email):
            print(f"Low priority email: {email}")
            verified_emails.append({'query': email, 'status': 'RECEIVING', 'priority': 'low'})
        else:
            print(f"Invalid or low priority email: {email}")
            verified_emails.append({'query': email, 'status': 'INVALID', 'priority': 'none'})

    return verified_emails


def insert_vendor_data(collection, category, final_url, result, valid_links_by_category):
    print(f"Inserting data for link: {final_url}")
    category_label, score = classify_text(result['combined_text'], categories)
    if category_label != "No confident classification result.":
        result['classification'] = {
            'category': category_label,
            'score': score
        }
        weight = calculate_weight(result)
        result['weight'] = weight
        collection.insert_one(result)
        valid_links_by_category[category].append(final_url)
    else:
        print(f"Classification not confident for link: {final_url}")

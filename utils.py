from urllib.parse import urlparse
from transformers import pipeline
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import categories
import validators


def ensure_url_scheme(url):
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url


def get_final_url(driver, initial_url):
    try:
        initial_url = ensure_url_scheme(initial_url)

        if not validators.url(initial_url):
            print(f"Invalid initial URL format: {initial_url}")
            return None

        print(f"Navigating to {initial_url}...")
        driver.get(initial_url)
        final_url = driver.current_url

        if final_url.startswith("http") and validators.url(final_url):
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
    # if doc.get('emails', [{'value': ''}])[0]['value']:
        # filled_fields += 10
    if doc.get('emails') and doc['emails'][0].get('value', ''):
        filled_fields += 10
    # if doc.get('phones', [{'value': ''}])[0]['value']:
        # filled_fields += 10
    if doc.get('phones') and doc['phones'][0].get('value', ''):
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


# this will compare the collection with data collection and create a new collection with deleted duplicates

def update_new_collection(collection_name):
    db = connect_to_mongo()
    if db is None:
        return

    data_collection = db['data']
    new_collection = db[collection_name]

    existing_vendors = set(doc['query'].strip().lower() for doc in data_collection.find({}, {'query': 1}))

    new_vendors = []
    for item in new_collection.find({}):
        website = item.get('query', '').strip().lower()
        if website not in existing_vendors:
            new_vendors.append(item)

    updated_collection_name = collection_name + '_updated'
    db[updated_collection_name].drop()

    if new_vendors:
        db[updated_collection_name].insert_many(new_vendors)

    create_excel_file(updated_collection_name)
    print("New collection updated and duplicates removed. New collection 'new_collection_updated' created.")


# create a data collection in mongo from collections already exist, check if there is any duplicate by looking query

from db import connect_to_mongo
from excel import create_excel_file


def merge_collections():
    db = connect_to_mongo()
    if db is None:
        return

    collection_names = [name for name in db.list_collection_names() if name != 'data']

    all_data = []
    seen_queries = set()
    for collection_name in collection_names:
        collection = db[collection_name]
        for item in collection.find({}):
            if item['query'] not in seen_queries:
                seen_queries.add(item['query'])
                all_data.append(item)

    db['data'].drop()

    new_collection = db['data']
    if all_data:
        new_collection.insert_many(all_data)

    print("Data merged and duplicates removed based on 'query'. New collection 'data' created.")
    create_excel_file('data')


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

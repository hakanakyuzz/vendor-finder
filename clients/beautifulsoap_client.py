import json
import requests
from bs4 import BeautifulSoup
import re

def scrape_vendor_data(final_url):
    try:
        print(f"Scraping data for vendor link: {final_url}")

        retries = 3
        timeout = 10
        for attempt in range(retries):
            try:
                response = requests.get(final_url, timeout=timeout)
                response.raise_for_status()
                break  # Exit the loop if the request is successful
            except requests.exceptions.RequestException as e:
                print(f"Error scraping {final_url}: {e}")
                if attempt + 1 == retries:
                    print(f"Failed to retrieve data after {retries} attempts, moving on...")
                    return None
                print("Retrying...")

        soup = BeautifulSoup(response.content, 'html.parser')

        emails = set()
        for mailto in soup.select('a[href^=mailto]'):
            email = mailto.get('href').replace('mailto:', '').strip()
            emails.add(email)

        phone_numbers = set()
        phone_pattern = re.compile(r'\+?\d[\d\s\-()]{7,}\d')
        for text in soup.stripped_strings:
            if phone_pattern.search(text):
                phone_numbers.add(phone_pattern.search(text).group())

        socials = {}
        for social in soup.select('a[href^="https://twitter.com"], a[href^="https://www.facebook.com"], a[href^="https://www.linkedin.com"], a[href^="https://www.instagram.com"], a[href^="https://www.youtube.com"]'):
            if 'twitter' in social['href']:
                socials['twitter'] = social['href']
            elif 'facebook' in social['href']:
                socials['facebook'] = social['href']
            elif 'linkedin' in social['href']:
                socials['linkedin'] = social['href']
            elif 'instagram' in social['href']:
                socials['instagram'] = social['href']
            elif 'youtube' in social['href']:
                socials['youtube'] = social['href']

        description = soup.find('meta', attrs={'name': 'description'})
        description_content = description['content'] if description else ''

        country = ''
        city = ''

        for text in soup.stripped_strings:
            if 'Country' in text:
                country = text.split(':')[-1].strip()
            if 'City' in text:
                city = text.split(':')[-1].strip()

        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            json_data = json.loads(script.string)
            address = json_data.get('address', {})
            if isinstance(address, dict):
                country = address.get('addressCountry', country)
                city = address.get('addressLocality', city)

        result = {
            'query': final_url,
            'emails': [{'value': email} for email in emails],
            'phones': [{'value': phone} for phone in phone_numbers],
            'site_data': {
                'description': description_content,
            },
            'socials': socials,
            'details': {
                'country': country,
                'city': city
            },
            'classification': {
                'category': '',
                'score': 0.0
            },
            'weight': 0.0
        }

        print(f"Results for {final_url}: {result}")
        return [result]

    except Exception as e:
        print(f"Failed to scrape {final_url}: {e}")
        return None


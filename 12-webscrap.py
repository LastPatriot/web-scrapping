import requests
from bs4 import BeautifulSoup
import sys
import json
import csv

def fetch_html_content(url):
    """
    Fetches the HTML content from the given URL.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL '{url}': {e}", file=sys.stderr)
        return None

def extract_data(html_content, selector_map):
    """
    Parses the HTML content and extracts data based on a dictionary of CSS selectors.
    """
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    extracted_records = []

    record_container_selector = selector_map.get('record_container_selector')

    if record_container_selector:
        containers = soup.select(record_container_selector)
        for container in containers:
            record = {}
            for field, selector_info in selector_map.items():
                if field == 'record_container_selector':
                    continue

                if isinstance(selector_info, dict):
                    selector = selector_info['selector']
                    attribute = selector_info.get('attribute')
                    element = container.select_one(selector)
                    if element and attribute:
                        record[field] = element.get(attribute, '').strip()
                    elif element:
                        record[field] = element.get_text(strip=True)
                    else:
                        record[field] = None
                else:
                    element = container.select_one(selector_info)
                    if element:
                        record[field] = element.get_text(strip=True)
                    else:
                        record[field] = None

            if record:
                extracted_records.append(record)
    else:
        print("Warning: No 'record_container_selector' provided. Extracting based on individual selectors, which might not group data logically.", file=sys.stderr)
        record = {}
        for field, selector_info in selector_map.items():
            if isinstance(selector_info, dict):
                selector = selector_info['selector']
                attribute = selector_info.get('attribute')
                elements = soup.select(selector)
                if elements:
                    if attribute:
                        record[field] = [e.get(attribute, '').strip() for e in elements if e.get(attribute)]
                    else:
                        record[field] = [e.get_text(strip=True) for e in elements]
                else:
                    record[field] = []
            else:
                elements = soup.select(selector_info)
                if elements:
                    record[field] = [e.get_text(strip=True) for e in elements]
                else:
                    record[field] = []
        if record:
            extracted_records.append(record)

    return extracted_records

def save_data(data, output_format="json", filename="extracted_data"):
    """
    Saves the extracted data to a file in the specified format.
    """
    if not data:
        print("No data to save.", file=sys.stderr)
        return

    if output_format.lower() == "json":
        full_filename = f"{filename}.json"
        try:
            with open(full_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Data saved to {full_filename}")
        except IOError as e:
            print(f"Error saving JSON data to '{full_filename}': {e}", file=sys.stderr)
    elif output_format.lower() == "csv":
        full_filename = f"{filename}.csv"
        try:
            headers = data[0].keys()
            with open(full_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            print(f"Data saved to {full_filename}")
        except IOError as e:
            print(f"Error saving CSV data to '{full_filename}': {e}", file=sys.stderr)
        except IndexError:
            print("Error: Data is empty or malformed for CSV conversion.", file=sys.stderr)
    else:
        print(f"Unsupported output format: '{output_format}'. Choose 'json' or 'csv'.", file=sys.stderr)

if __name__ == "__main__":
    DEFAULT_URL = "https://www.google.com/search?q=python+web+scraping"

    GOOGLE_SEARCH_SELECTORS = {
        'record_container_selector': 'div.g',
        'title': 'h3',
        'link': {'selector': 'a', 'attribute': 'href'},
        'snippet': 'div.IsZzjf'
    }

    TARGET_SELECTORS = GOOGLE_SEARCH_SELECTORS

    url = DEFAULT_URL
    output_filename = "extracted_data"
    output_format = "json"

    if len(sys.argv) > 1:
        url = sys.argv[1]
    if len(sys.argv) > 2:
        output_filename = sys.argv[2]
    if len(sys.argv) > 3:
        output_format = sys.argv[3].lower()

    print(f"Scraping data from: {url}")
    print(f"Output will be saved to: {output_filename}.{output_format}")

    html = fetch_html_content(url)

    if html:
        data = extract_data(html, TARGET_SELECTORS)
        if data:
            print(f"Extracted {len(data)} records.")
            save_data(data, output_format, output_filename)
        else:
            print("No data extracted. Check selectors or URL.", file=sys.stderr)
    else:
        print("Failed to retrieve HTML content.", file=sys.stderr)

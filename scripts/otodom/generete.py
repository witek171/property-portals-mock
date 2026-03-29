from pathlib import Path
import json
import re

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data' / 'otodom'
DOCS_DIR = PROJECT_ROOT / 'docs' / 'otodom'
DOCS_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://localhost:8000/otodom"
OFFERS_PER_PAGE = 24
REDIRECT_PAGES = 1


def extract_json_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', content, re.DOTALL)

    if not match:
        raise ValueError(f"Not found JSON-LD in {file_path}")

    return json.loads(match.group(1))


def create_html(json_data, title="Mock"):
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <script type="application/ld+json">
{json.dumps(json_data, indent=2, ensure_ascii=False)}
    </script>
</head>
<body></body>
</html>
'''


def create_redirect_html(target_url):
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url={target_url}">
    <title>Przekierowanie...</title>
</head>
<body>
    <p>Przekierowanie na <a href="{target_url}">{target_url}</a></p>
</body>
</html>
'''


try:
    listing_source = extract_json_from_html(DATA_DIR / 'listing.html')
except FileNotFoundError:
    exit(1)

all_offers = listing_source['@graph'][1]['offers']['offers']

for i, offer in enumerate(all_offers, 1):
    offer['url'] = f"{BASE_URL}/oferta-{i}.html"

total_pages = (len(all_offers) + OFFERS_PER_PAGE - 1) // OFFERS_PER_PAGE

if total_pages == 1:
    last_page_filename = "listing.html"
else:
    last_page_filename = f"listing-page-{total_pages}.html"

for page_num in range(1, total_pages + 1):
    start = (page_num - 1) * OFFERS_PER_PAGE
    end = start + OFFERS_PER_PAGE

    page_offers = all_offers[start:end]

    page_data = json.loads(json.dumps(listing_source))
    page_data['@graph'][1]['offers']['offers'] = page_offers

    if page_num == 1:
        filename = 'listing.html'
    else:
        filename = f'listing-page-{page_num}.html'

    page_data['@graph'][0]['url'] = f"{BASE_URL}/{filename}"

    html = create_html(page_data, f"Otodom - Strona {page_num}")

    with open(DOCS_DIR / filename, 'w', encoding='utf-8') as f:
        f.write(html)

redirect_target = f"{BASE_URL}/{last_page_filename}"

for page_num in range(total_pages + 1, total_pages + REDIRECT_PAGES + 1):
    filename = f"listing-page-{page_num}.html"

    html = create_redirect_html(redirect_target)

    with open(DOCS_DIR / filename, 'w', encoding='utf-8') as f:
        f.write(html)

for i, offer in enumerate(all_offers, 1):
    offer_data = json.loads(json.dumps(listing_source))
    offer_data['@graph'][1]['offers']['offers'] = [offer]
    offer_data['@graph'][0]['url'] = f"{BASE_URL}/oferta-{i}.html"

    offer_name = offer.get('name', f'Oferta {i}')
    filename = f'oferta-{i}.html'

    html = create_html(offer_data, offer_name)

    with open(DOCS_DIR / filename, 'w', encoding='utf-8') as f:
        f.write(html)

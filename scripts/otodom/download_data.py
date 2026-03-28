from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
import json
import time

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data' / 'otodom'

driver = webdriver.Chrome()

try:
    listing_url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie%2Crynek-wtorny/cala-polska?limit=72"
    driver.get(listing_url)
    time.sleep(3)

    scripts = driver.find_elements(By.XPATH, '//script[@type="application/ld+json"]')
    listing_json = scripts[0].get_attribute('innerHTML')
    listing_data = json.loads(listing_json)

    with open(DATA_DIR / 'listing.json', 'w', encoding='utf-8') as f:
        json.dump(listing_data, f, indent=2, ensure_ascii=False)

    offer_url = "https://www.otodom.pl/pl/oferta/2-pokojowe-z-balkonem-wyposazone-przytulne-ID4AIgX"
    driver.get(offer_url)
    time.sleep(3)

    scripts = driver.find_elements(By.XPATH, '//script[@type="application/ld+json"]')
    offer_json = scripts[0].get_attribute('innerHTML')
    offer_data = json.loads(offer_json)

    with open(DATA_DIR / 'offer.json', 'w', encoding='utf-8') as f:
        json.dump(offer_data, f, indent=2, ensure_ascii=False)

finally:
    driver.quit()

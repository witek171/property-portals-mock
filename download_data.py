from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

print("🚀 Uruchamiam przeglądarkę...")

# Uruchom Chrome
driver = webdriver.Chrome()

try:
    # Wejdź na stronę listingu
    url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska"
    print(f"📡 Pobieram: {url}")
    driver.get(url)

    # Poczekaj aż strona się załaduje
    time.sleep(3)

    # Znajdź wszystkie tagi <script type="application/ld+json">
    scripts = driver.find_elements(By.XPATH, '//script[@type="application/ld+json"]')

    print(f"✅ Znaleziono {len(scripts)} tagów JSON-LD")

    # Pierwszy tag zawiera dane listingu
    listing_json = scripts[0].get_attribute('innerHTML')
    listing_data = json.loads(listing_json)

    # Zapisz
    with open('listing.json', 'w', encoding='utf-8') as f:
        json.dump(listing_data, f, indent=2, ensure_ascii=False)

    print("✅ Zapisano listing.json")

    # Pobierz URL pierwszej oferty
    offers = listing_data['@graph'][1]['offers']['offers']
    first_offer_url = offers[0]['url']

    print(f"\n📡 Pobieram ofertę: {first_offer_url}")
    driver.get(first_offer_url)
    time.sleep(3)

    # Znajdź JSON-LD na stronie oferty
    scripts = driver.find_elements(By.XPATH, '//script[@type="application/ld+json"]')
    offer_json = scripts[0].get_attribute('innerHTML')
    offer_data = json.loads(offer_json)

    # Zapisz
    with open('offer_template.json', 'w', encoding='utf-8') as f:
        json.dump(offer_data, f, indent=2, ensure_ascii=False)

    print("✅ Zapisano offer_template.json")
    print("\n🎉 Gotowe! Możesz teraz uruchomić: python generate.py")

finally:
    driver.quit()
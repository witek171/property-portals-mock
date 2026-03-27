import json

# =============================================================================
# WCZYTAJ DANE
# =============================================================================

with open('listing.json', 'r', encoding='utf-8') as f:
    listing_data = json.load(f)

with open('offer_template.json', 'r', encoding='utf-8') as f:
    offer_template = json.load(f)

# =============================================================================
# PRZYGOTUJ DANE
# =============================================================================

all_offers = listing_data['@graph'][1]['offers']['offers']

OFFERS_PER_PAGE = 10
pages = []

for i in range(0, len(all_offers), OFFERS_PER_PAGE):
    page_offers = all_offers[i:i + OFFERS_PER_PAGE]
    pages.append(page_offers)

print(f"📦 Będę generować:")
print(f"   - {len(pages)} stron listingu")
print(f"   - {len(all_offers)} pojedynczych ofert\n")

# =============================================================================
# SŁOWNIK: która oferta jest na której stronie (do nawigacji powrotnej)
# =============================================================================

offer_to_page = {}  # {numer_oferty: numer_strony}
offer_counter = 1

for page_num, page_offers in enumerate(pages, 1):
    for _ in page_offers:
        offer_to_page[offer_counter] = page_num
        offer_counter += 1

# =============================================================================
# GENERUJ STRONY LISTINGU
# =============================================================================

offer_counter = 1

for page_num, page_offers in enumerate(pages, 1):

    if page_num == 1:
        filename = "listing.html"
    else:
        filename = f"listing-page-{page_num}.html"

    listing_html = f'''<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <title>Mieszkania na sprzedaż - Strona {page_num}</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
    h1 {{ color: #333; }}
    .stats {{ color: #666; margin-bottom: 20px; }}
    .offer-card {{ background: white; border: 1px solid #ddd; padding: 20px; margin: 15px 0; border-radius: 8px; }}
    .offer-card h2 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 18px; }}
    .price {{ font-size: 24px; font-weight: bold; color: #27ae60; margin: 10px 0; }}
    .location {{ color: #7f8c8d; margin: 5px 0; font-size: 15px; }}
    .location .district {{ color: #555; font-weight: 500; }}
    .details {{ color: #95a5a6; font-size: 14px; margin: 10px 0; }}
    .btn {{ display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px; }}
    .pagination {{ text-align: center; margin: 40px 0; padding: 20px; background: white; border-radius: 8px; }}
    .pagination a, .pagination .current {{ display: inline-block; margin: 0 5px; padding: 8px 15px; border-radius: 5px; text-decoration: none; }}
    .pagination a {{ background: #3498db; color: white; }}
    .pagination a:hover {{ background: #2980b9; }}
    .pagination .current {{ background: #95a5a6; color: white; }}
  </style>
</head>
<body>
  <h1>🏠 Mieszkania na sprzedaż</h1>
  <p class="stats">Strona {page_num} z {len(pages)} | Wyświetlono oferty {(page_num - 1) * OFFERS_PER_PAGE + 1}-{min(page_num * OFFERS_PER_PAGE, len(all_offers))} z {len(all_offers)}</p>

  <div class="offers-list">
'''

    temp_counter = offer_counter
    for offer in page_offers:
        name = offer.get('name', 'Bez tytułu')
        price = offer.get('price', 0)

        item = offer.get('itemOffered', {})
        address = item.get('address', {})

        # Pobierz wszystkie elementy adresu
        street = address.get('streetAddress', '')
        district = address.get('name', '')  # DZIELNICA
        city = address.get('addressLocality', '')
        region = address.get('addressRegion', '')

        # Buduj lokalizację hierarchicznie
        location_parts = []

        if street:
            location_parts.append(f'ul. {street}')

        # Dzielnica + miasto
        city_part = []
        if district:
            city_part.append(district)
        if city:
            city_part.append(city)

        if city_part:
            location_parts.append(', '.join(city_part))

        if region:
            location_parts.append(region)

        location = ', '.join(location_parts) if location_parts else 'brak lokalizacji'

        rooms = item.get('numberOfRooms', '?')
        floor_size = item.get('floorSize', {}).get('value', '?')

        if isinstance(price, (int, float)) and price > 0:
            price_str = f"{price:,.0f}".replace(",", " ")
        else:
            price_str = "Zapytaj o cenę"

        offer['url'] = f'http://localhost:8000/oferta-{temp_counter}.html'

        listing_html += f'''
    <div class="offer-card">
      <h2>{name}</h2>
      <div class="price">{price_str} zł</div>
      <div class="location">📍 {location}</div>
      <div class="details">🛏️ {rooms} pokoje | 📐 {floor_size} m²</div>
      <a href="oferta-{temp_counter}.html" class="btn">Zobacz szczegóły</a>
    </div>
'''
        temp_counter += 1

    listing_html += '''
  </div>

  <div class="pagination">
'''

    if page_num > 1:
        prev_file = "listing.html" if page_num == 2 else f"listing-page-{page_num - 1}.html"
        listing_html += f'<a href="{prev_file}">← Poprzednia</a>'

    for p in range(1, len(pages) + 1):
        if p == page_num:
            listing_html += f'<span class="current">{p}</span>'
        else:
            page_file = "listing.html" if p == 1 else f"listing-page-{p}.html"
            listing_html += f'<a href="{page_file}">{p}</a>'

    if page_num < len(pages):
        listing_html += f'<a href="listing-page-{page_num + 1}.html">Następna →</a>'

    listing_html += '''
  </div>

  <script type="application/ld+json">
'''

    page_data = json.loads(json.dumps(listing_data))
    page_data['@graph'][1]['offers']['offers'] = page_offers
    page_data['@graph'][1]['offers']['offerCount'] = str(len(all_offers))

    listing_html += json.dumps(page_data, indent=2, ensure_ascii=False)
    listing_html += '''
  </script>
</body>
</html>
'''

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(listing_html)

    print(f"✅ {filename} (oferty {offer_counter}-{temp_counter - 1})")

    offer_counter = temp_counter

# =============================================================================
# GENERUJ POJEDYNCZE OFERTY
# =============================================================================

print(f"\n📄 Generuję pojedyncze oferty...\n")

offer_counter = 1

for page_offers in pages:
    for offer in page_offers:

        single_offer_data = json.loads(json.dumps(offer_template))
        product = single_offer_data['@graph'][1]

        name = offer.get('name', 'Bez tytułu')
        price = offer.get('price', 0)

        product['name'] = name
        product['url'] = f'http://localhost:8000/oferta-{offer_counter}.html'
        product['offers']['price'] = price

        if 'itemOffered' in offer:
            item = offer['itemOffered']

            if 'address' in item:
                product['address'] = item['address']
            if 'numberOfRooms' in item:
                product['numberOfRooms'] = item['numberOfRooms']
            if 'description' in item:
                product['description'] = item['description']

            floor_value = item.get('floorSize', {}).get('value', '?')
        else:
            floor_value = '?'

        # Buduj lokalizację Z DZIELNICĄ
        address = product.get('address', {})

        street = address.get('streetAddress', '')
        district = address.get('name', '')  # DZIELNICA
        city = address.get('addressLocality', '')
        region = address.get('addressRegion', '')

        location_parts = []

        if street:
            location_parts.append(f'ul. {street}')
        if district:
            location_parts.append(district)
        if city:
            location_parts.append(city)
        if region:
            location_parts.append(region)

        location = ', '.join(location_parts) if location_parts else 'Brak lokalizacji'

        rooms = product.get('numberOfRooms', '?')
        description = product.get('description', 'Brak opisu')

        if '<' in description:
            from bs4 import BeautifulSoup

            description = BeautifulSoup(description, 'html.parser').get_text()

        if isinstance(price, (int, float)) and price > 0:
            price_str = f"{price:,.0f}".replace(",", " ")
        else:
            price_str = "Zapytaj o cenę"

        # WAŻNE: Link powrotny do właściwej strony listingu
        page_num = offer_to_page[offer_counter]
        if page_num == 1:
            back_link = "listing.html"
        else:
            back_link = f"listing-page-{page_num}.html"

        offer_html = f'''<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <title>{name}</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
    .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
    h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; margin-bottom: 20px; }}
    .price {{ font-size: 36px; font-weight: bold; color: #27ae60; margin: 20px 0; }}
    .info {{ background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }}
    .info-item {{ margin: 12px 0; font-size: 16px; line-height: 1.6; }}
    .label {{ font-weight: bold; color: #34495e; display: inline-block; min-width: 160px; }}
    .value {{ color: #555; }}
    .description {{ line-height: 1.8; color: #555; margin: 25px 0; padding: 20px; background: #f9f9f9; border-left: 4px solid #3498db; }}
    .description h2 {{ color: #2c3e50; margin-top: 0; }}
    .back-link {{ display: inline-block; margin-top: 30px; padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }}
    .back-link:hover {{ background: #2980b9; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{name}</h1>

    <div class="price">💰 {price_str} zł</div>

    <div class="info">
      <div class="info-item">
        <span class="label">📍 Lokalizacja:</span>
        <span class="value">{location}</span>
      </div>
      <div class="info-item">
        <span class="label">🛏️ Liczba pokoi:</span>
        <span class="value">{rooms}</span>
      </div>
      <div class="info-item">
        <span class="label">📐 Powierzchnia:</span>
        <span class="value">{floor_value} m²</span>
      </div>
'''

        if 'additionalProperty' in product:
            for prop in product['additionalProperty'][:5]:
                prop_name = prop.get('name', '')
                prop_value = prop.get('value', '')
                if prop_name and prop_value:
                    offer_html += f'''
      <div class="info-item">
        <span class="label">• {prop_name}:</span>
        <span class="value">{prop_value}</span>
      </div>
'''

        offer_html += f'''
    </div>

    <div class="description">
      <h2>Opis</h2>
      <p>{description[:1000]}{"..." if len(description) > 1000 else ""}</p>
    </div>

    <a href="{back_link}" class="back-link">← Powrót do wyników (strona {page_num})</a>
  </div>

  <script type="application/ld+json">
{json.dumps(single_offer_data, indent=2, ensure_ascii=False)}
  </script>
</body>
</html>
'''

        with open(f'oferta-{offer_counter}.html', 'w', encoding='utf-8') as f:
            f.write(offer_html)

        print(f"✅ oferta-{offer_counter}.html (→ {back_link}) - {name[:50]}...")

        offer_counter += 1

print("\n" + "=" * 70)
print("🎉 GOTOWE!")
print("=" * 70)
print(f"\n📁 Wygenerowano:")
print(f"   • {len(pages)} stron listingu")
print(f"   • {offer_counter - 1} pojedynczych ofert")
print(f"\n🚀 Uruchom: python -m http.server 8000")
print(f"🌐 Otwórz: http://localhost:8000/listing.html")
print("=" * 70)
# Property Portals Mock

Statyczne mocki polskich portali nieruchomości do testowania scraperów.

---

## O projekcie
Projekt generuje statyczne strony HTML z danymi, imitujące prawdziwe portale nieruchomości (np. Otodom, OLX). 

**Cel:** Testowanie scraperów bez obciążania produkcyjnych stron.

## Funkcjonalności
- Pobieranie realnych danych z portali
- Generowanie stron listingów
- Generowanie pojedynczych stron ofert
- Automatyczne przekierowania
- Minimalistyczny HTML

---

## Testuj lokalnie
```
cd docs
py -m http.server 8000
```
Listing URL: 

http://localhost:8000/otodom/listing.html

http://localhost:8000/otodom/listing-page-2.html ...

Offer URL:

http://localhost:8000/otodom/mieszkanie-2-pokojowe-bemowo-wszedzie-blisko-ID4AhfS.html

---

## Portale
### Otodom:
**Dane:** JSON-LD w <script type="application/ld+json">

**External ID:** Wyciągane z URL oferty (np. `...mieszkanie-3-pok-ID4AIgX` → `ID4AIgX`)

**Wykrywanie usuniętych ofert:** Usunięta → nie zawiera <script type="application/ld+json">

**Paginacja:** Strona poza zakresem → redirect na ostatnią

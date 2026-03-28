from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
import json
import time

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data' / 'otodom'
DATA_DIR.mkdir(parents=True, exist_ok=True)


def download_and_save(driver, url, filename):
    driver.get(url)
    time.sleep(3)

    scripts = driver.find_elements(By.XPATH, '//script[@type="application/ld+json"]')

    if not scripts:
        return False

    json_content = scripts[0].get_attribute('innerHTML')
    data = json.loads(json_content)

    html = f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <script type="application/ld+json">
{json.dumps(data, indent=2, ensure_ascii=False)}
    </script>
</head>
<body></body>
</html>
'''

    with open(DATA_DIR / filename, 'w', encoding='utf-8') as f:
        f.write(html)

    return True


driver = webdriver.Chrome()

try:
    download_and_save(
        driver,
        "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie%2Crynek-wtorny/cala-polska?limit=72",
        "listing.html")

    download_and_save(
        driver,
        "https://www.otodom.pl/pl/oferta/2-pokojowe-z-balkonem-wyposazone-przytulne-ID4AIgX",
        "offer.html")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()

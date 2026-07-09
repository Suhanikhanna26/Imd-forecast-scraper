from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
import time
import os

# -------------------------------
# Configure Chrome for GitHub Actions
# -------------------------------

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

# -------------------------------
# Open IMD Mumbai Colaba page
# -------------------------------

driver.get(
    "https://city.imd.gov.in/citywx/responsive/?id=43057"
)

# Wait for React page to load
time.sleep(10)

# -------------------------------
# Find forecast cards
# -------------------------------

cards = driver.find_elements(
    By.CSS_SELECTOR,
    "div.min-h-32.relative.p-4.rounded-lg.shadow.bg-slate-100"
)

records = []

# -------------------------------
# Extract forecast information
# -------------------------------

for card in cards:
    try:
        date = card.find_element(
            By.CSS_SELECTOR,
            "span.text-blue-700"
        ).text

        temp_text = card.find_element(
            By.CSS_SELECTOR,
            "h3.text-sm.font-semibold.text-blue-600"
        ).text

        temps = temp_text.split()

        max_temp = temps[0].replace("°", "")
        min_temp = temps[1].replace("°", "")

        forecast = card.find_element(
            By.CSS_SELECTOR,
            "p.text-gray-600"
        ).text

        warning = card.find_element(
            By.CSS_SELECTOR,
            "div.text-xs.text-white"
        ).text

        records.append({
            "scrape_time": datetime.now(),
            "station": "Mumbai-Colaba",
            "forecast_date": date,
            "max_temp": max_temp,
            "min_temp": min_temp,
            "forecast": forecast,
            "warning": warning
        })

    except Exception as e:
        print(f"Skipping card due to error: {e}")

# Close browser
driver.quit()

# -------------------------------
# Save to CSV
# -------------------------------

df = pd.DataFrame(records)

os.makedirs("data", exist_ok=True)

file_exists = os.path.exists("data/imd_forecast.csv")

df.to_csv(
    "data/imd_forecast.csv",
    mode="a",
    header=not file_exists,
    index=False
)

print("\nSuccessfully scraped IMD forecast data:")
print(df)
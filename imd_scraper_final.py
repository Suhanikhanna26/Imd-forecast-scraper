from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import time

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.get(
    "https://city.imd.gov.in/citywx/responsive/?id=43057"
)

time.sleep(10)

cards = driver.find_elements(
    By.CSS_SELECTOR,
    "div.min-h-32.relative.p-4.rounded-lg.shadow.bg-slate-100"
)

records = []

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
        print(e)

driver.quit()

df = pd.DataFrame(records)

df.to_csv(
    "data/imd_forecast.csv",
    mode="a",
    header=not os.path.exists("data/imd_forecast.csv"),
    index=False
)

print(df)
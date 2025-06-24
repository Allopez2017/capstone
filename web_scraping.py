from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

url = "https://www.baseball-almanac.com/ws/wsmenu.shtml"

def scrape(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        data_table = driver.find_element(By.TAG_NAME, "table")
        rows = data_table.find_elements(By.TAG_NAME, "tr")[2:]

        data = []
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            row_data = [column.text.strip() for column in columns]
            if row_data:
                data.append(row_data)

        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        print(f"An error occured, unable to scrape data: {e}")

    finally:
        driver.quit()

df = scrape(url)
if df is not None:
        df.to_csv("world_series.csv", index=False)
        print("Data saved to csv file")

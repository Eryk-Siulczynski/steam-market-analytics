import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://store.steampowered.com/search/results/"

params = {
    "query": "",
    "start": 0,
    "count": 100,
    "sort_by": "_ASC",
    "filter": "topsellers",
    "supportedlang": "english",
    "infinite": 1
}

response = requests.get(url, params=params)
data = response.json()

html = data["results_html"]

soup = BeautifulSoup(html, "html.parser")

rows = soup.select("a.search_result_row")

results = []

for index, row in enumerate(rows, start=1):
    appid = row.get("data-ds-appid")
    title = row.select_one(".title")

    results.append({
        "rank": index,
        "appid": int(appid),
        "name": title.text.strip() if title else None
    })

df = pd.DataFrame(results)



today = datetime.now().strftime("%Y-%m-%d")

dated_filename = f"Data/Raw/top_sellers_{today}.csv"
latest_filename = "Data/Raw/top_sellers_latest.csv"

df["snapshot_date"] = today

print(df)

df.to_csv(dated_filename, index=False, encoding="utf-8-sig")
df.to_csv(latest_filename, index=False, encoding="utf-8-sig")

import requests
import pandas as pd
import time
from datetime import datetime

top = pd.read_csv("Data/Raw/top_sellers_latest.csv")
appids = top["appid"].tolist()

results = []

for appid in appids:
    print(f"Processing {appid}")

    # -------------------
    # APP DETAILS
    # -------------------
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=de&l=english"
    response = requests.get(url)
    data = response.json()

    game_data = data[str(appid)]

    if game_data["success"]:

        game = game_data["data"]

        genres = game.get("genres", [])
        genre_names = ", ".join([g["description"] for g in genres])

        categories = game.get("categories", [])
        category_names = ", ".join([c["description"] for c in categories])

        dlc_count = len(game.get("dlc", []))

        price = game.get("price_overview", {})
        metacritic = game.get("metacritic", {})

        # -------------------
        # REVIEWS
        # -------------------
        review_url = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all&purchase_type=all"

        review_response = requests.get(review_url)
        review_data = review_response.json()

        summary = review_data.get("query_summary", {})

        positive = summary.get("total_positive", 0)
        negative = summary.get("total_negative", 0)
        reviews_count = positive + negative

        if reviews_count > 0:
            positive_percent = round((positive / reviews_count) * 100, 2)
        else:
            positive_percent = None

        # -------------------
        # CURRENT PLAYERS
        # -------------------
        players_url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"

        players_response = requests.get(players_url)
        players_data = players_response.json()

        current_players = players_data.get("response", {}).get("player_count")

        # -------------------
        # SAVE RESULT
        # -------------------
        results.append({
            "appid": appid,
            "name": game.get("name"),
            "is_free": game.get("is_free"),
            "genres": genre_names,
            "recommendations": game.get("recommendations", {}).get("total"),
            "release_date": game.get("release_date", {}).get("date"),
            "price_final": price.get("final", 0) / 100 if price.get("final") is not None else None,
            "price_initial": price.get("initial", 0) / 100 if price.get("initial") is not None else None,
            "currency": price.get("currency"),
            "discount_percent": price.get("discount_percent"),
            "metacritic_score": metacritic.get("score"),
            "categories": category_names,
            "dlc_count": dlc_count,
            "reviews_count": reviews_count,
            "positive_percent": positive_percent,
            "current_players": current_players
        })

    time.sleep(1)

df = pd.DataFrame(results)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

print(df)

final_df = top.merge(df, on="appid", how="left")

print(final_df)



today = datetime.now().strftime("%Y-%m-%d")
final_df["snapshot_date"] = today
filename = f"Data/Processed/steam_market_{today}.csv"
final_df.to_csv(filename, index=False, encoding="utf-8-sig")

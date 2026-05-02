import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
processed_folder = BASE_DIR / "Data" / "Processed"

snapshot_files = list(processed_folder.glob("steam_market_*.csv"))

# Pomijamy latest i history, żeby nie dublować danych
snapshot_files = [
    file for file in snapshot_files
    if "latest" not in file.name and "history" not in file.name
]

all_data = []

for file in snapshot_files:
    print(f"Reading: {file.name}")

    df = pd.read_csv(file)

    # Awaryjnie: jeśli kiedyś zabraknie snapshot_date, bierzemy datę z nazwy pliku
    if "snapshot_date" not in df.columns:
        date_from_filename = file.stem.replace("steam_market_", "")
        df["snapshot_date"] = date_from_filename

    all_data.append(df)

if all_data:
    history_df = pd.concat(all_data, ignore_index=True)

    # Usuwamy ewentualne duplikaty: ta sama data + ta sama gra
    history_df = history_df.drop_duplicates(
        subset=["snapshot_date", "appid"],
        keep="last"
    )

    # Sortowanie: data, potem rank
    history_df = history_df.sort_values(
        by=["snapshot_date", "rank"],
        ascending=[True, True]
    )

    output_file = processed_folder / "steam_market_history.csv"

    history_df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"History file created: {output_file}")
    print(history_df.shape)

else:
    print("No snapshot files found.")

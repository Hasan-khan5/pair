import requests
import json
import os

def append_new_data(market_names):
    for market in market_names:
        try:
            # Step 1: Fetch new-day data
            api = f"https://cbi.gammaxbd.xyz/qxfetch.php?pair={market}-OTC&days=1"
            response = requests.get(api)
            response.raise_for_status()
            new_data = response.json()

            if not new_data:
                print(f"No data returned for {market}")
                continue

            # Step 2: Load old data if exists
            filename = f"{market}-OTC.json"
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    old_data = json.load(f)
            else:
                old_data = []

            # Step 3: Determine the unique key (assume 't' for timestamp)
            unique_key = "t"

            # Collect existing timestamps
            old_timestamps = {item[unique_key] for item in old_data if unique_key in item}

            # Filter new candles not already in file
            unique_new_data = [item for item in new_data if item.get(unique_key) not in old_timestamps]

            if unique_new_data:
                combined_data = old_data + unique_new_data
                with open(filename, 'w') as f:
                    json.dump(combined_data, f, indent=2)
                print(f"{filename}: Added {len(unique_new_data)} new entries.")
            else:
                print(f"{filename}: No new unique data to add.")

        except Exception as e:
            print(f"Error updating {market}: {e}")

# Example usage with multiple market pairs
#market_names = ["BRLUSD", "BTCUSD", "INTL", "MCD", "MSFT", "JNJ",  "USDBDT", "USDINR", "USDEGP", "XAUUSD", "USDMXN", "USDNGN", "USDTRY", "USDPKR", "USDIDR", "USDARS", "BA", "AXP", "FB", "PFE" ]
market_names = ["BRLUSD"]
append_new_data(market_names)

import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

# Short URL provided for tracking
SHORT_URL = "https://c.org/wbMkDmC2KT"

def get_signatures():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # Resolve shortlink and get the final URL page content
        response = requests.get(SHORT_URL, headers=headers, timeout=15)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Pull tracking text embedded inside social meta tags
        meta_tag = soup.find("meta", property="og:description")
        if meta_tag:
            text_content = meta_tag["content"]
            # Filter and join only digit characters found before the sign word indicator
            digits = "".join(filter(str.isdigit, text_content.split("signed")))
            if digits:
                return int(digits)
        return None
    except Exception as e:
        print(f"Tracking error: {e}")
        return None

def update_database(current_count):
    file_name = "petition_data.csv"
    file_exists = os.path.isfile(file_name)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    last_count = current_count
    if file_exists:
        with open(file_name, "r") as f:
            lines = list(csv.reader(f))
            if len(lines) > 1:
                # Reference previous total to measure velocity change
                last_count = int(lines[-1][1])
                
    hourly_growth = current_count - last_count
    
    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Total Signatures", "Hourly Growth"])
        writer.writerow([timestamp, current_count, hourly_growth])

if __name__ == "__main__":
    count = get_signatures()
    if count:
        update_database(count)
        print(f"Database successfully synced. Current total: {count}")
    else:
        print("Data extraction failed during this run interval.")

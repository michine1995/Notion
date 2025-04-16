# notion_upload.py
import csv
import os
import requests

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
CSV_FILE_PATH = "meta_csv/riahouse_meta_report.csv"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_page(row):
    return {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Date": {"date": {"start": row[0]}},
            "Campaign": {"title": [{"text": {"content": row[1]}}]},
            "Cost": {"number": float(row[2])},
            "CPM": {"number": float(row[3])},
            "CTR": {"number": float(row[4])},
            "CPC": {"number": float(row[5])},
            "Impressions": {"number": int(float(row[6]))},
            "Link Clicks": {"number": int(float(row[7]))},
            "Conversions": {"number": int(float(row[8]))}
        }
    }

def upload_csv_to_notion():
    if not os.path.exists(CSV_FILE_PATH):
        print(f"❌ ファイルが見つかりません: {CSV_FILE_PATH}")
        return

    with open(CSV_FILE_PATH, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            page_data = create_page(row)
            response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=page_data)
            if response.status_code != 200:
                print("❌ Error:", response.text)
            else:
                print("✅ Row uploaded:", row[1])

if __name__ == "__main__":
    upload_csv_to_notion()

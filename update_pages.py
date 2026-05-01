import os
import itertools
import urllib.parse
import pandas as pd
import requests

# あなたの正規のAmazonアソシエイトID
AMAZON_ID = "gearguide0c85-20"
OUTPUT_DIR = "docs"

# 1. 確実な手動データ（人気モデル）
canon_devices = ['EOS R5', 'EOS R6', 'EOS R3', 'EOS R10', 'EOS R50', 'EOS R8', 'EOS 90D', 'EOS 850D']
nikon_devices = ['Z9', 'Z8', 'Z7 II', 'Z6 II', 'Zf', 'Zfc', 'Z50', 'Z30']

# 2. Wikipediaからの自動抽出エンジン（Sony用）
def fetch_sony_devices():
    try:
        url = "https://en.wikipedia.org/wiki/List_of_Sony_E-mount_cameras"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        tables = pd.read_html(response.text)
        for df in tables:
            if "Model" in df.columns:
                devices = df["Model"].dropna().astype(str).tolist()
                return [d.split('[')[0].strip() for d in devices if len(d) > 3 and "Model" not in d]
    except Exception as e:
        print(f"Scraping Error: {e}")
    return []

# 3. データの統合
sony_devices = fetch_sony_devices()
all_devices = list(set(canon_devices + nikon_devices + sony_devices))

accessories = [
    {"type": "SD Card"}, {"type": "Screen Protector"}, 
    {"type": "Extra Battery"}, {"type": "Camera Bag"}, 
    {"type": "Tripod"}, {"type": "Cleaning Kit"}, {"type": "Lens Cap"}
]

# 4. ページ生成ロジック（本物のアソシエイトIDを使用）
os.makedirs(OUTPUT_DIR, exist_ok=True)
count = 0

for device, accessory in itertools.product(all_devices, accessories):
    safe_name = "".join(c if c.isalnum() else "-" for c in f"{device}-{accessory['type']}").lower().strip("-")
    file_path = os.path.join(OUTPUT_DIR, f"best-{safe_name}.md")
    
    query = f"{device} {accessory['type']}"
    amazon_url = f"https://www.amazon.com/s?k={urllib.parse.quote_plus(query)}&tag={AMAZON_ID}"
    
    content = f"""---
title: "Best {accessory['type']} for {device} in 2026"
---
# Best {accessory['type']} for {device}

If you own a **{device}**, finding the right **{accessory['type']}** is critical.
👉 [See the Best-Selling {accessory['type']}s for {device} on Amazon]({amazon_url})
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1

print(f"✅ {count} pages successfully generated and updated.")

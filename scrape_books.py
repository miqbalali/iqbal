import requests
from bs4 import BeautifulSoup
import json
import csv
import os
from datetime import datetime

def scrape_crypto():
    url = "https://coinmarketcap.com/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    crypto_data = []
    
    # Cari tabel crypto
    table = soup.find('table')
    
    if not table:
        print("Tabel tidak ditemukan")
        return []
    
    rows = table.find_all('tr')[1:21]  # Ambil 20 crypto teratas
    
    for idx, row in enumerate(rows, 1):
        try:
            # Nama crypto
            name_elem = row.find('p', class_='coin-item-name')
            if not name_elem:
                name_elem = row.find('span', class_='crypto-symbol')
            
            name = name_elem.get_text(strip=True) if name_elem else f"Crypto {idx}"
            
            # Harga
            price_elem = row.find('span', class_='price')
            price = price_elem.get_text(strip=True) if price_elem else "N/A"
            
            # Market cap
            market_cap_elem = row.find('span', class_='market-cap')
            market_cap = market_cap_elem.get_text(strip=True) if market_cap_elem else "N/A"
            
            crypto_data.append({
                'no': idx,
                'nama': name,
                'harga_usd': price,
                'market_cap': market_cap,
                'sumber': 'CoinMarketCap',
                'waktu_scraping': str(datetime.now())
            })
            
            print(f"{idx}. {name} - {price}")
            
        except Exception as e:
            print(f"Error pada baris {idx}: {e}")
            continue
    
    return crypto_data

def save_files(data):
    os.makedirs('hasil_crypto', exist_ok=True)
    
    with open('hasil_crypto/crypto.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    with open('hasil_crypto/crypto.csv', 'w', newline='', encoding='utf-8') as f:
        if data:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    print(f"\n✅ Data disimpan di folder 'hasil_crypto/'")

def main():
    print("💰 Scraping Crypto Prices...")
    print("-" * 40)
    data = scrape_crypto()
    
    if data:
        print(f"\n📊 Total: {len(data)} cryptocurrency")
        save_files(data)
        print("\n✨ Selesai!")
    else:
        print("❌ Gagal mengambil data")

if __name__ == "__main__":
    main()
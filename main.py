import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all_sites(site_list):
    # Browser အပြင်မှာ မမြင်ရအောင် ပိတ်ထားမယ် (Headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    all_live_links = {}

    for site_url in site_list:
        print(f"ရှာဖွေနေသည်: {site_url} ...")
        try:
            driver.get(site_url)
            time.sleep(5) # Website ပွင့်ဖို့နဲ့ JavaScript အလုပ်လုပ်ဖို့ ခဏစောင့်မယ်
            
            page_source = driver.page_source
            # .m3u8 လင့်ခ်တွေကို ပုံစံထုတ်ပြီး ရှာမယ်
            links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', page_source)
            
            if links:
                all_live_links[site_url] = list(set(links))
                print(f"တွေ့ရှိမှု: {len(links)} ခု ရရှိသည်။")
            else:
                print("လင့်ခ်အသစ် မတွေ့ပါ။")
                
        except Exception as e:
            print(f"Error တက်နေသည် {site_url}: {e}")

    driver.quit()
    return all_live_links

# သင်ရှာချင်တဲ့ Website ၅ ခုလောက်ကို ဒီအောက်မှာ ထည့်ပါ
my_target_sites = [
    "https://example-sports-1.com",
    "https://example-sports-2.com",
    "https://burmese.live",
    "https://another-live-site.net"
]

# စတင်လုပ်ဆောင်ခြင်း
results = scrape_all_sites(my_target_sites)

print("\n--- စုစည်းရရှိထားသော Live Links များ ---")
for site, links in results.items():
    print(f"\nWebsite: {site}")
    for l in links:
        print(f"  > {l}")

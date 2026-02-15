from flask import Flask, jsonify
import requests
import re

app = Flask(__name__)

# Browser အယောင်ဆောင်ဖို့ (Blocking မဖြစ်အောင်)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_live_links():
    target_sites = [
        "https://m.yuyantv.cn/", 
        "https://www.thscore.mobi/",
        "https://www.98sports.com/",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/mm.m3u" # မြန်မာလိုင်းများ (Test ရန်)
    ]
    
    found_links = []
    
    for site in target_sites:
        try:
            # timeout ကို ၈ စက္ကန့်အထိ တိုးထားတယ်၊ Headers ပါထည့်ထားတယ်
            r = requests.get(site, headers=HEADERS, timeout=8)
            
            # m3u8 link တွေကို ရှာမယ်
            links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r.text)
            
            for l in links:
                # မလိုအပ်တဲ့ link တွေ (ဥပမာ- ads link) တွေကို စစ်ချင်ရင် ဒီမှာ စစ်လို့ရတယ်
                if "m3u8" in l:
                    found_links.append({
                        "title": f"Live from {site.split('//')[1].split('/')[0]}",
                        "url": l,
                        "source": site
                    })
        except:
            continue
            
    # အကယ်၍ ဘာလင့်ခ်မှ မတွေ့ရင် ပြမယ့် dummy data (စမ်းသပ်ရန်)
    if not found_links:
        return [{"title": "No Live Matches", "url": "", "source": "System"}]
        
    return found_links

@app.route('/')
def home():
    data = scrape_live_links()
    return jsonify(data)

if __name__ == "__main__":
    # Render အတွက် Port က dynamic ဖြစ်နိုင်လို့ environment ကနေ ဖတ်တာ ပိုစိတ်ချရတယ်
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

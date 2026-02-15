from flask import Flask, jsonify
import requests
import re
import os

app = Flask(__name__)

# Browser အယောင်ဆောင်ရန် Header (Block မဖြစ်စေရန်)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_live_links():
    # Live ပွဲစဉ်များ ရနိုင်ခြေအရှိဆုံး Website စာရင်း
    target_sites = [
        "https://m.yuyantv.cn/", 
        "https://www.thscore.mobi/",
        "https://www.98sports.com/",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/mm.m3u" # မြန်မာလိုင်းများ စမ်းသပ်ရန်
    ]
    
    found_links = []
    
    for site in target_sites:
        try:
            # Website တစ်ခုချင်းစီကို ဝင်နှိုက်ခြင်း
            r = requests.get(site, headers=HEADERS, timeout=8)
            
            # .m3u8 လင့်ခ်များကို ပုံစံထုတ်ပြီး ရှာဖွေခြင်း
            links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r.text)
            
            for l in links:
                # ဒေတာများကို သပ်သပ်ရပ်ရပ် သိမ်းဆည်းခြင်း
                found_links.append({
                    "title": f"Live Link from {site.split('//')[1].split('/')[0]}",
                    "url": l,
                    "source": site
                })
        except:
            continue
            
    # အကယ်၍ လင့်ခ်အသစ် မတွေ့သေးပါက ပြသရန် နမူနာဒေတာ
    if not found_links:
        return [{"title": "Data Updating... No Live Matches Found Yet", "url": "", "source": "System"}]
        
    return found_links

@app.route('/')
def home():
    # API ခေါ်ယူသည့်အခါ function ကို run ပေးခြင်း
    data = scrape_live_links()
    return jsonify(data)

if __name__ == "__main__":
    # Render ပေါ်တွင် အလုပ်လုပ်နိုင်ရန် Port ကို dynamic ထားခြင်း
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

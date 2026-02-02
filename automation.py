import os
import json
import subprocess
import cloudinary
import cloudinary.uploader
import cloudinary.api

# 1. Cloudinary कॉन्फ़िगरेशन
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

# 2. आपकी धांसू कैटेगरीज़
CATEGORIES = {
    "Life_Lessons": "deep life lesson movie scenes hindi shorts",
    "Motivational": "best motivational status clips hindi",
    "Sad_Dramas": "Pakistani drama emotional dialogue status",
    "Attitude_Killer": "South movie attitude entry status hindi",
    "Podcast_Clips": "viral podcast clips hindi life lessons",
    "News_Debates": "funny and aggressive news debate moments status"
}

def fetch_from_youtube():
    """YouTube से ट्रेंडिंग वीडियो डाउनलोड करके Cloudinary पर अपलोड करना"""
    print("--- चरण 1: YouTube से कंटेंट अपलोड हो रहा है ---")
    for folder, query in CATEGORIES.items():
        cmd = [
            'yt-dlp', f"ytsearch1:{query}", 
            '--format', 'best[ext=mp4]', 
            '--max-filesize', '15M', 
            '--match-filter', 'duration < 65', 
            '--output', 'temp_status.mp4', '--no-playlist'
        ]
        try:
            subprocess.run(cmd, check=True)
            # यहाँ हमने 'StatusMagic/' फोल्डर फिक्स कर दिया है
            cloudinary.uploader.upload(
                "temp_status.mp4", 
                resource_type="video", 
                folder=f"StatusMagic/{folder}",
                tags=[folder, "auto_youtube"]
            )
            print(f"✅ सफलता: {folder} का वीडियो अपलोड हुआ।")
            if os.path.exists("temp_status.mp4"):
                os.remove("temp_status.mp4")
        except Exception as e:
            print(f"❌ गड़बड़ ({folder}): {e}")

def update_json_list():
    """Cloudinary के हर कोने से सभी 66+ वीडियो निकालकर JSON फाइल बनाना"""
    print("--- चरण 2: Cloudinary से पूरी लिस्ट निकाली जा रही है ---")
    video_list = []
    try:
        # यहाँ हमने max_results=500 रखा है ताकि आपके सभी 66 वीडियो एक साथ आ जाएँ
        # 'prefix' का इस्तेमाल करके हम पूरे StatusMagic फोल्डर को खंगालेंगे
        response = cloudinary.api.resources(
            resource_type="video", 
            type="upload", 
            prefix="StatusMagic", 
            max_results=500 
        )
        
        for asset in response.get('resources', []):
            video_list.append({
                "url": asset['secure_url'],
                "public_id": asset['public_id']
            })

        # अगर कुछ बाहर (Root) छूट गया हो, तो उसे भी ले लो (जैसे आपके 2 मैन्युअल वीडियो)
        root_response = cloudinary.api.resources(resource_type="video", type="upload", max_results=100)
        for asset in root_response.get('resources', []):
            # डुप्लीकेट और सैंपल वीडियो को हटाना
            if "samples/" not in asset['public_id'] and not any(v['public_id'] == asset['public_id'] for v in video_list):
                video_list.append({
                    "url": asset['secure_url'],
                    "public_id": asset['public_id']
                })

        # ताज़ा लिस्ट को videos.json में लिखना
        with open('videos.json', 'w') as f:
            json.dump(video_list, f, indent=4)
        
        print(f"🚀 मिशन पूरा! अब आपकी वेबसाइट पर कुल {len(video_list)} वीडियो दिखेंगे।")
    except Exception as e:
        print(f"❌ JSON अपडेट फेल: {e}")

if __name__ == "__main__":
    fetch_from_youtube()
    update_json_list()

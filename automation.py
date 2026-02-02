import os
import json
import subprocess
import cloudinary
import cloudinary.uploader
import cloudinary.api

# 1. Cloudinary सेटअप (GitHub Secrets से चाबियाँ उठाएगा)
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
    """YouTube से ट्रेंडिंग वीडियो ढूंढकर अपलोड करना"""
    print("--- YouTube से माल (Content) खोजना शुरू ---")
    for folder, query in CATEGORIES.items():
        print(f"प्रोसेसिंग कैटेगरी: {folder}")
        
        # yt-dlp का इस्तेमाल (हर कैटेगरी का 1 सबसे बेस्ट वीडियो)
        cmd = [
            'yt-dlp',
            f"ytsearch1:{query}", 
            '--format', 'best[ext=mp4]', 
            '--max-filesize', '15M', 
            '--match-filter', 'duration < 65', 
            '--output', 'temp_status.mp4',
            '--no-playlist'
        ]
        
        try:
            subprocess.run(cmd, check=True)
            # Cloudinary पर सही फोल्डर में अपलोड करना
            cloudinary.uploader.upload(
                "temp_status.mp4", 
                resource_type="video", 
                folder=f"StatusMagic/{folder}",
                tags=[folder, "auto_youtube"]
            )
            print(f"सफलता: {folder} का नया वीडियो अपलोड हुआ।")
            if os.path.exists("temp_status.mp4"):
                os.remove("temp_status.mp4")
        except Exception as e:
            print(f"वीडियो स्किप हुआ ({folder}): {e}")

def update_json_list():
    """Cloudinary के सभी 66+ वीडियो को videos.json में लाना"""
    print("--- Cloudinary से पूरी लिस्ट निकालना (JSON Update) ---")
    try:
        # हमने सर्च को 'Open' रखा है ताकि आपके सभी 66 वीडियो मिलें
        resources = cloudinary.api.resources(
            resource_type="video", 
            type="upload", 
            max_results=500 
        )
        
        video_list = []
        for asset in resources.get('resources', []):
            # केवल असली वीडियो चुनें, सैंपल वीडियो को छोड़ दें
            if "samples/" not in asset['public_id']:
                video_list.append({
                    "url": asset['secure_url'],
                    "public_id": asset['public_id']
                })
        
        # ताज़ा लिस्ट को videos.json फाइल में लिखना
        with open('videos.json', 'w') as f:
            json.dump(video_list, f, indent=4)
        
        print(f"बधाई! videos.json अपडेट हो गई। कुल वीडियो: {len(video_list)}")
    except Exception as e:
        print(f"JSON अपडेट के दौरान गड़बड़: {e}")

if __name__ == "__main__":
    fetch_from_youtube() # 1. पहले नए वीडियो लाओ
    update_json_list()   # 2. फिर पूरी लिस्ट को वेबसाइट के लिए अपडेट करो

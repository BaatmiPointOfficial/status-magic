import os
import subprocess
import cloudinary
import cloudinary.uploader

# Cloudinary Setup (आपके सुरक्षित 'Secrets' से चाबियाँ उठाएगा)
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

# आपकी सभी पसंदीदा कैटेगरीज और उनके स्मार्ट सर्च कीवर्ड्स
CATEGORIES = {
    "Life_Lessons": "deep life lesson movie scenes hindi shorts",
    "Motivational": "best motivational status clips hindi",
    "Sad_Dramas": "Pakistani drama emotional dialogue status",
    "Attitude_Killer": "South movie attitude entry status hindi",
    "Podcast_Clips": "viral podcast clips hindi life lessons",
    "News_Debates": "funny and aggressive news debate moments status"
}

def download_and_upload():
    for folder, query in CATEGORIES.items():
        print(f"--- {folder} कैटेगरी पर काम शुरू ---")
        
        # yt-dlp के साथ हाई-क्वालिटी 'जुगाड़'
        # यह हर कैटेगरी का 1 सबसे वायरल 'Short' वीडियो उठाएगा
        cmd = [
            'yt-dlp',
            f"ytsearch1:{query}", 
            '--format', 'best[ext=mp4]', # सबसे अच्छी क्वालिटी
            '--max-filesize', '15M', # साइज कंट्रोल
            '--match-filter', 'duration < 65', # सिर्फ छोटे स्टेटस वीडियो
            '--output', 'temp_status.mp4',
            '--no-playlist'
        ]
        
        try:
            # वीडियो डाउनलोड करना
            subprocess.run(cmd, check=True)
            print(f"वीडियो डाउनलोड हो गया: {folder}")

            # Cloudinary पर सही फोल्डर में अपलोड करना
            upload_result = cloudinary.uploader.upload(
                "temp_status.mp4",
                resource_type="video",
                folder=f"StatusMagic/{folder}", # अलग-अलग फोल्डर बनेंगे
                tags=[folder, "StatusMagic_Auto"]
            )
            print(f"सफलता! Cloudinary लिंक: {upload_result['secure_url']}")
            
            # काम होने के बाद फाइल डिलीट करना
            if os.path.exists("temp_status.mp4"):
                os.remove("temp_status.mp4")
                
        except Exception as e:
            print(f"त्रुटि ({folder}): {e}") # एरर लॉगिंग

if __name__ == "__main__":
    download_and_upload()

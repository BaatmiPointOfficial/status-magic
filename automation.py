import cloudinary
import cloudinary.api
import json
import os

# Cloudinary Configuration
cloudinary.config(
  cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
  api_key = os.environ.get('CLOUDINARY_API_KEY'),
  api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

def fetch_videos():
    # यह लाइन अब बिना टैग के सारे वीडियो ढूँढेगी
    results = cloudinary.api.resources(resource_type = "video", max_results = 500)
    videos = []
    for res in results.get('resources', []):
        videos.append({
            "url": res['secure_url'],
            "public_id": res['public_id']
        })
    
    with open('videos.json', 'w') as f:
        json.dump(videos, f, indent=4)

if __name__ == "__main__":
    fetch_videos()

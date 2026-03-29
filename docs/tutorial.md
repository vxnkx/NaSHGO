# NaSHGO - OSINT Geolocation Tool

## 🎯 What It Does
1. Harvests public images from Instagram/Flickr/Twitter  
2. Extracts GPS EXIF coordinates
3. Reverse geocodes → addresses/cities
4. Finds nearby Shodan devices (IoT/cameras)
5. Telegram alerts + interactive HTML maps

## 🚀 Quickstart (60 seconds)
```bash
git clone <repo> && cd GeoImageHarvester
pip install -r requirements.txt
cp config.example.yaml config.yaml
echo "natgeo elonmusk" > data/usernames.txt
python run.py natgeo elonmusk

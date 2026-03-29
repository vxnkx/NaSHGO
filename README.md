# NaSHGO OSINT Geolocation Tool

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
```
⚙️ Config Setup
```bash
# 1. Get free API keys
curl https://account.shodan.io/api-key  # Copy to config.yaml
@BotFather /newbot → Get telegram_bot_token
```
# 2. Edit config.yaml (gitignored)
```bash
vim config.yaml  # Add your keys + Tor proxy
```
# 3. Tor proxy (optional opsec)
```bash
docker run -d -p 9050:9050 oberthur/docker-tor
```
📋 Full Workflow
```bash
$ python run.py target1 target2 --telegram
```

[+] Harvesting target1 (30 images)
✅ GEOLOCATED: target1 (30.123456, -97.654321) → "123 Main St, Austin TX"
📱 Telegram: QR code to interactive map sent
📊 Report: output/georeport.html

Pro Tips

# Stealth mode (Tor + slow rate limit)
rate_limit: 5.0
proxies: socks5://127.0.0.1:9050

# Max speed
max_threads: 10
rate_limit: 0.5
# Shodan nearby cameras
shodan_radius_km: 2.0

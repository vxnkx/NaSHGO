# NaSHGO
osint-geo-exif-harvester
**OPSEC-aware image geolocation OSINT tool**

Harvests Instagram/Flickr images → extracts EXIF GPS → Shodan IoT overlay → Interactive map

1. **Copy config**:
```bash
cp config.example.yaml config.yaml
nano config.yaml  # Edit 4 lines ONLY 👇
```

2. add your keys:
```bash
shodan_api_key: "your_key"           # shodan.io (FREE)
telegram_bot_token: "bot_token"      # @BotFather 
telegram_chat_id: "123456789"        # Message bot /start
proxies.http: "socks5://127.0.0.1:9050"  # Tor optional
```

3. Tor (optional OPSEC):
```bash
docker run -d --name tor -p 9050:9050 oberthur/docker-tor
```

3. Run:
```bash
python run.py elonmusk --telegram
```

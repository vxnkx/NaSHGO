# NaSHGO
osint-geo-exif-harvester
**OPSEC-aware image geolocation OSINT tool**

Harvests Instagram/Flickr images → extracts EXIF GPS → Shodan IoT overlay → Interactive map

## Quickstart
```bash
cp config.example.yaml config.yaml  # Add Shodan key/proxies
pip install -r requirements.txt
python run.py @target1 @target2 -o myreport
opsec: Tor proxy recommended, randomized UAs, rate-limited.

## **Usage**
```bash
# Copy config, add Shodan key
cp config.example.yaml config.yaml

# Harvest
python run.py john_doe jane_smith -o target_report

# With Tor (docker run -p 9050:9050 -d torproject/tor)
python run.py @target -c config.yaml

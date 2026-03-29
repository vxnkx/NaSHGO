import os
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import yaml
from .exif import extract_gps_from_image
from .geocode import geocode_coords, shodan_nearby_devices

class GeoImageHarvester:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.session = requests.Session()
        self.ua_list = self.config['user_agents']
        self.proxies = self.config.get('proxies', {})
        self.rate_limit = self.config['rate_limit']
        self.max_threads = self.config['max_threads']
        self.session.proxies.update(self.proxies)
        self.results = []
        self.shodan_api = self.config.get('shodan_api_key')

    def _random_headers(self):
        return {
            'User-Agent': random.choice(self.ua_list),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def _rate_sleep(self):
        time.sleep(self.rate_limit + random.uniform(0.1, 0.5))

    def instagram_images(self, username, max_images=50):
        """Harvest Instagram public images (no login required)"""
        images = []
        url = f"https://www.instagram.com/{username}/"
        
        resp = self.session.get(url, headers=self._random_headers())
        if resp.status_code != 200:
            return images
            
        # Extract JSON from Instagram page
        script_pattern = r'window\._sharedData = ({.*?});'
        match = re.search(script_pattern, resp.text)
        if match:
            data = json.loads(match.group(1))
            edges = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
            
            for edge in edges[:max_images]:
                img_url = edge['node']['thumbnail_src']
                images.append(img_url)
        
        return images

    def flickr_images(self, username, max_images=50):
        """Harvest Flickr public images"""
        images = []
        url = f"https://www.flickr.com/photos/{username}/"
        
        resp = self.session.get(url, headers=self._random_headers())
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for img in soup.find_all('img', {'data-context': True})[:max_images]:
            src = img.get('src') or img.get('data-src')
            if src and 'staticflickr.com' in src:
                images.append(src)
        
        return images

    def download_and_extract(self, img_url, target_dir):
        """Download image + extract GPS (thread-safe)"""
        try:
            fname = os.path.basename(img_url.split('?')[0])
            path = os.path.join(target_dir, fname)
            
            resp = self.session.get(img_url, headers=self._random_headers(), timeout=15)
            if resp.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(resp.content)
                
                gps = extract_gps_from_image(path)
                if gps:
                    location = geocode_coords(gps['lat'], gps['lon'])
                    devices = shodan_nearby_devices(gps['lat'], gps['lon'], self.shodan_api) if self.shodan_api else []
                    
                    self.results.append({
                        'url': img_url,
                        'file': path,
                        'gps': gps,
                        'location': location,
                        'shodan_devices': devices[:5]  # Top 5 nearby
                    })
                    return True
        except Exception:
            pass
        return False

    def harvest_target(self, target_usernames, output_dir="output"):
        """Full harvest workflow"""
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
        
        all_images = []
        for username in tqdm(target_usernames, desc="Harvesting profiles"):
            print(f"[+] Harvesting {username}")
            all_images.extend(self.instagram_images(username))
            all_images.extend(self.flickr_images(username))
            self._rate_sleep()
        
        # Dedupe & download
        unique_images = list(set(all_images))
        print(f"[+] Found {len(unique_images)} unique images")
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            list(tqdm(executor.map(
                lambda url: self.download_and_extract(url, os.path.join(output_dir, "images")),
                unique_images
            ), total=len(unique_images), desc="Processing images"))
        
        print(f"[+] Found {len(self.results)} geolocated images")
        return self.results

# CLI Entry (also imported by run.py)
def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('usernames', nargs='+', help="Instagram/Flickr usernames")
    parser.add_argument('-o', '--output', default='output')
    parser.add_argument('-c', '--config', default='config.yaml')
    args = parser.parse_args()
    
    harvester = GeoImageHarvester(args.config)
    results = harvester.harvest_target(args.usernames, args.output)
    from .report import generate_html_report
    generate_html_report(results, f"{args.output}/georeport.html")
    print(f"[+] Report: {args.output}/georeport.html")

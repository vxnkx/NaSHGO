from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import shodan

geolocator = Nominatim(user_agent="geo_harvester")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def geocode_coords(lat, lon):
    """Reverse geocode with fallback"""
    try:
        location = geocode((lat, lon))
        return {
            'address': location.address if location else 'Unknown',
            'city': location.raw.get('address', {}).get('city', 'Unknown'),
            'country': location.raw.get('address', {}).get('country', 'Unknown')
        }
    except:
        return {'address': 'Geocode failed', 'city': 'Unknown', 'country': 'Unknown'}

def shodan_nearby_devices(lat, lon, api_key, radius=0.1):
    """Find IoT/devices within radius"""
    if not api_key:
        return []
    try:
        shodan.Shodan(api_key).search(f"city:near:{lat},{lon},{radius}")
        # Simplified - full impl uses geo: bounding box
        return ["Shodan query would return nearby cams/IP cams here"]
    except:
        return []

import exifread
import math

def extract_gps_from_image(image_path):
    """Extract GPS coords from EXIF with opsec (no disk writes)"""
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, stop_tag='GPS GPSLatitude')
        
        lat = _gps_to_decimal(getattr(tags.get('GPS GPSLatitude'), 'values', []))
        lon = _gps_to_decimal(getattr(tags.get('GPS GPSLongitude'), 'values', []))
        
        if lat and lon:
            return {
                'lat': lat,
                'lon': lon,
                'accuracy': float(tags.get('GPS GPSDOP', '0').values[0]) if 'GPS GPSDOP' in tags else 0
            }
    except:
        pass
    return None

def _gps_to_decimal(gps_coords):
    """Convert DMS to decimal degrees"""
    if len(gps_coords) < 3 or not gps_coords[0]:
        return None
    return float(gps_coords[0]) + float(gps_coords[1])/60 + float(gps_coords[2])/3600

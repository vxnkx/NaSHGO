import pytest
import yaml
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
sys.path.insert(0, 'src')

# Import your existing modules
from core import GeoImageHarvester  
from exif import extract_gps_from_image
from geocode import geocode_coords

@pytest.fixture
def sample_config():
    return yaml.safe_load("""
general:
  user_agent: "test"
  rate_limit_delay: 0
  max_workers: 1
sources:
  instagram: {enabled: true, max_posts: 5}
telegram:
  enabled: false
    """)

def test_extract_gps_from_image():
    """Test your existing EXIF function"""
    result = extract_gps_from_image("nonexistent.jpg")
    assert result is None  # No file = no GPS

def test_geocode_coords():
    """Test your geocode function"""
    result = geocode_coords(40.7128, -74.0060)
    assert 'address' in result
    assert result['city'] != 'Unknown'  # Should geocode NYC

@patch('requests.Session.get')
def test_instagram_harvest(mock_get, sample_config):
    """Test Instagram harvesting"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '{"entry_data":{"ProfilePage":[{"graphql":{"user":{"edge_owner_to_timeline_media":{"edges":[{"node":{"thumbnail_src":"https://i.imgur.com/test.jpg"}}]}}}}]}}'
    
    harvester = GeoImageHarvester(sample_config)
    images = harvester.instagram_public_images("testuser")
    assert len(images) == 1

def test_full_pipeline(tmp_path):
    """Test complete workflow"""
    config = {"general": {"max_workers": 1}}
    harvester = GeoImageHarvester(config)
    
    with patch('src.exif.extract_gps_from_image') as mock_exif, \
         patch('src.geocode.geocode_coords') as mock_geo:
        
        mock_exif.return_value = {'lat': 40.71, 'lon': -74.00}
        mock_geo.return_value = {'address': 'New York, NY'}
        
        result = harvester.process_image(
            "https://example.com/test.jpg", 
            "testuser", 
            "instagram", 
            tmp_path
        )
    
    assert result is not None
    assert result['gps']['lat'] == 40.71

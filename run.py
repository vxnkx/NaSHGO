#!/usr/bin/env python3
"""
NaSHGO CLI - Full opsec/osint geolocation tool
"""
import os
import sys
import asyncio
from argparse import ArgumentParser
import importlib.util

# dynamic import for modules
def load_module(path):
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["src.core"] = module
    spec.loader.exec_module(module)
    return module

# load core
core = load_module("src/core.py")

def main():
    parser = ArgumentParser(description="GeoImageHarvester - Image Geolocation OSINT")
    parser.add_argument('usernames', nargs='+', help="Instagram/Flickr usernames (e.g. 'elonmusk')")
    parser.add_argument('-o', '--output', default='output', help="Output directory")
    parser.add_argument('-c', '--config', default='config.yaml', help="Config file")
    parser.add_argument('--telegram', action='store_true', help="Send report to Telegram")
    parser.add_argument('--no-shodan', action='store_true', help="Skip Shodan queries")
    args = parser.parse_args()
    
    print("🗺️  GeoImageHarvester v1.0 - Starting...")
    
    # Initialize harvester
    harvester = core.GeoImageHarvester(args.config)
    
    # Harvest
    results = harvester.harvest_target(args.usernames, args.output)
    
    if not results:
        print("❌ No geolocated images found")
        return
    
    # Generate HTML report
    core.generate_html_report(results, f"{args.output}/georeport.html")
    print(f"📊 HTML Report: {args.output}/georeport.html")
    
    # Telegram (async)
    if args.telegram and harvester.config.get('telegram_bot_token'):
        print("📱 Sending Telegram report...")
        asyncio.run(harvester.send_telegram_report(args.usernames[0]))
    
    print(f"✅ Complete! Found {len(results)} geolocations")

if __name__ == "__main__":
    main()

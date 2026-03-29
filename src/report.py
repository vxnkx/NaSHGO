import folium
import json

def generate_html_report(results, output_path):
    """Interactive Leaflet map report"""
    if not results:
        return
    
    m = folium.Map(location=[results[0]['gps']['lat'], results[0]['gps']['lon']], zoom_start=12)
    
    for i, result in enumerate(results):
        folium.Marker(
            [result['gps']['lat'], result['gps']['lon']],
            popup=f"""
            <b>Image {i+1}</b><br>
            Location: {result['location']['address']}<br>
            <img src="{result['url']}" width="200"><br>
            Shodan: {len(result['shodan_devices'])} devices nearby
            """,
            tooltip=f"Image {i+1}"
        ).add_to(m)
    
    m.save(output_path)
    print(f"🌍 interactive map saved: {output_path}")

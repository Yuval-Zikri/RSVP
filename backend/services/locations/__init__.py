"""Location service for searching and geocoding locations."""
import requests


def search_location(query):
    """Search for location using Waze API
    
    Args:
        query: Search query string
        
    Returns:
        list: List of location results with label, x (lon), y (lat)
    """
    if not query:
        return []
        
    try:
        # Use a session to manage cookies
        session = requests.Session()
        
        # Headers from user's curl command
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.waze.com/he/live-map/directions',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        session.headers.update(headers)
        
        # 1. Visit the main page to get cookies (CSRF, etc.)
        # This is crucial as the user's curl had a _csrf_token cookie
        try:
            session.get('https://www.waze.com/he/live-map', timeout=5)
        except Exception as e:
            print(f"Failed to init session: {e}")

        # Waze Live Map Autocomplete API
        url = "https://www.waze.com/live-map/api/autocomplete/"
        params = {
            'q': query,
            'exp': '8,10,12',
            'geo-env': 'il',
            'lang': 'he',
            'v': '29.500000,34.000000;33.500000,36.000000' # Viewport covering Israel
        }
        
        response = session.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Waze API Error: {response.status_code} - {response.text}")
            return []
            
        data = response.json()
        
        results = []
        for item in data:
            if 'name' in item:
                label = item['name']
                # Fix: User output shows 'latLng' with 'lat' and 'lng'
                lat = item.get('latLng', {}).get('lat')
                lon = item.get('latLng', {}).get('lng')
                
                if lat and lon:
                    results.append({
                        'label': label,
                        'x': lon,
                        'y': lat,
                        'raw': item
                    })
            
        return results
    except Exception as e:
        print(f"Waze search error: {e}")
        return []


def reverse_geocode(lat, lng):
    """Convert coordinates to address using Nominatim
    
    Args:
        lat: Latitude
        lng: Longitude
        
    Returns:
        str: Address string or None if failed
    """
    try:
        response = requests.get(
            f"https://nominatim.openstreetmap.org/reverse",
            params={
                'format': 'json',
                'lat': lat,
                'lon': lng,
                'accept-language': 'he'
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('display_name')
        return None
    except Exception as e:
        print(f"Reverse geocoding error: {e}")
        return None

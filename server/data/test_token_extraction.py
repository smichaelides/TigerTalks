#!/usr/bin/env python3
"""
Test script to extract API token from registrar website
"""

import requests
import json
from bs4 import BeautifulSoup
import re

def test_token_extraction():
    """Test token extraction from registrar website"""
    url = "https://registrar.princeton.edu/course-offerings"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print("Fetching registrar page...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Success! Status code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Parsed HTML successfully")
        
        # Look for drupal-settings-json element
        print("\nLooking for drupal-settings-json element...")
        drupal_settings = soup.find(attrs={'data-drupal-selector': 'drupal-settings-json'})
        if drupal_settings and drupal_settings.text:
            print("Found drupal-settings-json element!")
            print(f"Content length: {len(drupal_settings.text)}")
            print(f"First 200 chars: {drupal_settings.text[:200]}")
            
            try:
                data = json.loads(drupal_settings.text)
                print("Successfully parsed JSON")
                print(f"Keys in data: {list(data.keys())}")
                
                if 'ps_registrar' in data:
                    print(f"ps_registrar keys: {list(data['ps_registrar'].keys())}")
                    if 'apiToken' in data['ps_registrar']:
                        token = data['ps_registrar']['apiToken']
                        print(f"Found API token: {token[:20]}...")
                        return token
                    else:
                        print("No apiToken found in ps_registrar")
                else:
                    print("No ps_registrar found in data")
                    
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
        else:
            print("No drupal-settings-json element found")
        
        # Fallback: regex search through all scripts
        print("\nSearching for API token in script tags...")
        script_count = 0
        for script in soup.find_all('script'):
            if script.string:
                script_count += 1
                match = re.search(r'"apiToken"\s*:\s*"([^"]+)"', script.string)
                if match:
                    token = match.group(1)
                    print(f"Found API token in script {script_count}: {token[:20]}...")
                    return token
        
        print(f"Searched {script_count} script tags, no API token found")
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    token = test_token_extraction()
    if token:
        print(f"\n✅ Successfully extracted token: {token}")
    else:
        print("\n❌ Failed to extract token")

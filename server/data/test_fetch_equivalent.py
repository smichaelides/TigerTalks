#!/usr/bin/env python3
"""
Python equivalent of JavaScript fetch to avoid 403 errors
"""

import requests
import json
from bs4 import BeautifulSoup
import re

def fetch_registrar_page():
    """Python equivalent of JavaScript fetch"""
    
    # Headers that closely mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    url = "https://registrar.princeton.edu/course-offerings"
    
    try:
        print("Making request with browser-like headers...")
        response = requests.get(url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Successfully fetched page!")
            print(f"Content length: {len(response.text)}")
            print(f"First 500 characters:")
            print(response.text[:500])
            print("\n" + "="*50)
            
            # Try to extract API token
            extract_api_token(response.text)
            return response.text
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def extract_api_token(html_content):
    """Extract API token from HTML content"""
    print("\n🔍 Searching for API token...")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Method 1: Look for drupal-settings-json element
    drupal_settings = soup.find(attrs={'data-drupal-selector': 'drupal-settings-json'})
    if drupal_settings and drupal_settings.text:
        print("Found drupal-settings-json element")
        try:
            data = json.loads(drupal_settings.text)
            if 'ps_registrar' in data and 'apiToken' in data['ps_registrar']:
                token = data['ps_registrar']['apiToken']
                print(f"✅ Found API token: {token[:20]}...")
                return token
        except json.JSONDecodeError as e:
            print(f"Failed to parse drupal settings: {e}")
    
    # Method 2: Search all script tags for apiToken
    print("Searching script tags for apiToken...")
    for i, script in enumerate(soup.find_all('script')):
        if script.string and 'apiToken' in script.string:
            print(f"Found potential token in script {i}")
            # Look for the token pattern
            match = re.search(r'"apiToken"\s*:\s*"([^"]+)"', script.string)
            if match:
                token = match.group(1)
                print(f"✅ Found API token in script: {token[:20]}...")
                return token
    
    print("❌ No API token found")
    return None

if __name__ == "__main__":
    print("Testing Python equivalent of JavaScript fetch...")
    html_content = fetch_registrar_page()
    
    if html_content:
        print("\n✅ Successfully fetched registrar page!")
    else:
        print("\n❌ Failed to fetch registrar page")

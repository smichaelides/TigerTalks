import requests

url = "https://registrar.princeton.edu/course-offerings"
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
data = ""
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.text
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")

print(data)
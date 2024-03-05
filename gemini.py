import json
import requests
API_KEY = "AIzaSyBE9CIN4RMUKl0qUcSScFr3avWbEUjUOos"
url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}'
headers = {'Content-Type': 'application/json'}
data = {
    "contents": [
        {
            "parts": [{"text": "請問你是誰？"}]
        }
    ]
}
response = requests.post(url, headers=headers, json=data)
print(f"response status_code: {response.status_code}")
print(json.dumps(response.json(), indent=4, ensure_ascii=False))



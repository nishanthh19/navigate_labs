import requests
import json
import re

with open("config.json") as f:
    config = json.load(f)

API_KEY = config["groq_api_key"]
MODEL = config.get("groq_model", "llama3-8b-8192")

def extract_meeting_info(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Extract the following details from this message:
- List of emails
- Start date (YYYY-MM-DD)
- Time (HH:MM 24hr format)
- Number of days

Message: "{user_input}"

Return ONLY this JSON structure (no explanation):
{{
  "emails": ["email1@example.com", "email2@example.com"],
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "days": <number>
}}
"""

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that extracts meeting scheduling info."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        # Show full response for debugging
        print("Groq API Response Code:", response.status_code)
        print("Groq API Response Text:", response.text)

        if response.status_code != 200:
            return {"error": f"Groq API Error {response.status_code}: {response.text}"}

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # Extract and parse the JSON from the content
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            return {"error": "Failed to extract JSON from model output."}

    except json.JSONDecodeError:
        return {"error": "Groq returned non-JSON response. Check API key or server status."}
    except Exception as e:
        return {"error": str(e)}

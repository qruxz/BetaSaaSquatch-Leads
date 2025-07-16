# email_writer.py using Groq
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama3-8b-8192"  # or try llama3-70b-8192

def generate_emails(company_name, info):
    description = info.get("description", "They are a growing company.")
    website = info.get("website", "N/A")
    linkedin = info.get("linkedin", "N/A")

    base_prompt = f"""
Company: {company_name}
Website: {website}
LinkedIn: {linkedin}
About: {description}

You're writing a cold outreach email to someone at this company.
Goal: Briefly and smartly introduce yourself, show relevance, and try to compliment or engage with them talk more and connect.
Keep it 3-4 sentences. Make it feel natural.
"""

    tones = {
        "friendly": "Write it like you're talking to someone cool you'd like to chat with. Slightly informal, warm, human.",
        "professional": "Write it like a smart business email approch. with smart simplerespectful, with a valuable proposal.",
        "casual": "Write it in a chill, creative fun way!. Feel free to be witty or unexpected, like a startup founder messaging another."
    }

    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    emails = {}

    for tone, style in tones.items():
        full_prompt = base_prompt + f"\nTone: {style}"

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are an expert cold outreach email writer."},
                {"role": "user", "content": full_prompt}
            ],
            "temperature": 0.8
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        try:
            data = response.json()
            print("🔍 Response:", json.dumps(data, indent=2))
            emails[tone] = data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"❌ Error generating {tone} email:", e)
            emails[tone] = f"⚠️ Could not generate {tone} email."

    return emails

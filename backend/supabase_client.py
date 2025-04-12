import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

def insert_question_to_supabase(text, summary, fake_score, explanation):
    payload = {
        "content": text,
        "summary": summary,
        "fake_score": fake_score,
        "explanation": explanation
    }

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/questions",
        json=payload,
        headers=headers
    )

    if response.status_code not in [200, 201]:
        print("Supabase Insert Error:", response.text)
        return False
    print("Connection successful and data inserted to Supabase.")   
    return True

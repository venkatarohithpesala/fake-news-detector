from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os
import requests
from supabase_client import insert_question_to_supabase  # Your custom DB function

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# Supabase Connection Function
def check_supabase_connection():
    headers = {
        "apikey": os.getenv("SUPABASE_API_KEY"),
        "Authorization": f"Bearer {os.getenv('SUPABASE_API_KEY')}"
    }

    url = f"{os.getenv('SUPABASE_URL')}/rest/v1/questions?select=id&limit=1"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code in [200, 206]:
            print("✅ Supabase connection successful.")
            return True
        else:
            print(f"Supabase connection failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print("Error connecting to Supabase:", e)
        return False


@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')

    prompt = f"""
You are a fake news checker assistant. A user will input a question, rumor, or headline.
Your task is to say whether it's likely to be true or false and explain briefly (2–3 sentences max).

Input:
{text}

Respond in plain English.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        explanation = response['choices'][0]['message']['content'].strip()
        summary = explanation[:150] + "..." if len(explanation) > 150 else explanation
        fake_score = 60  # Placeholder

        # Save to Supabase
        insert_success = insert_question_to_supabase(
            text=text,
            summary=summary,
            fake_score=fake_score,
            explanation=explanation
        )

        if not insert_success:
            return jsonify({"error": "Failed to save to database."}), 500

        return jsonify({
            "summary": summary,
            "fake_score": fake_score,
            "explanation": explanation
        })

    except Exception as e:
        print("OpenAI Error:", e)
        return jsonify({"error": "OpenAI API request failed."}), 500


# App entry point with Supabase connection check
if __name__ == '__main__':
    
    if not check_supabase_connection():
        print("Supabase is not connected. Exiting app.")
        exit(1)
    app.run(debug=True)

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
    user_input = data.get('text', '')

    # Step 1: Search NewsAPI with the user's input
    newsapi_key = os.getenv("NEWS_API_KEY")  # add to .env
    news_url = f"https://newsapi.org/v2/everything?q={user_input}&language=en&pageSize=3&apiKey={newsapi_key}"

    try:
        news_res = requests.get(news_url)
        news_data = news_res.json()

        if "articles" not in news_data:
            raise Exception("News API error or quota exceeded")

        top_articles = "\n\n".join([
            f"Title: {a['title']}\nSource: {a['source']['name']}\nSummary: {a['description'] or ''}" 
            for a in news_data["articles"]
        ])

        # Step 2: Prepare a powerful prompt with user input + search results
        prompt = f"""
You are a fact-checking assistant. A user has input a news claim. Analyze it using the latest news coverage below.

User Input:
{user_input}

Relevant News Articles:
{top_articles}

Your task is to assess whether the input is likely to be true or false.
Explain your reasoning clearly (2–3 sentences). Be concise and unbiased.

Respond in plain English.
"""

        # Step 3: Use OpenAI with upgraded context
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        explanation = response['choices'][0]['message']['content'].strip()
        summary = explanation[:150] + "..." if len(explanation) > 150 else explanation
        fake_score = 60  # Optional: improve later with sentiment/claim scoring

        # Save to Supabase
        insert_success = insert_question_to_supabase(
            text=user_input,
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
        print("Error:", e)
        return jsonify({"error": "Failed to analyze or fetch news."}), 500

# App entry point with Supabase connection check
if __name__ == '__main__':
    
    if not check_supabase_connection():
        print("Supabase is not connected. Exiting app.")
        exit(1)
    app.run(debug=True)

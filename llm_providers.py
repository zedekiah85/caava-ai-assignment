import json
import os
from openai import OpenAI

class OpenAIProvider:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        with open("categories.json") as f:
            self.categories = json.load(f)

    def classify(self, message: str) -> dict:
        category_definitions = "\n".join(
            [f"- {c['label']}: {c['description']}" for c in self.categories]
        )

        prompt = f"""
You are a customer support AI assistant. Categorize the following customer message into one of the categories listed below.

{category_definitions}

Message: "{message}"

Respond in valid JSON with:
- category (string)
- reasoning (string, optional)
- score (float between 0.0 and 1.0, optional)
- suggested_reply (string, optional)
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI customer service triage assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        reply = response.choices[0].message.content.strip()

        if reply.startswith("```json"):
            reply = reply.strip("```json").strip("```").strip()
        elif reply.startswith("```"):
            reply = reply.strip("```").strip()

        try:
            return json.loads(reply)
        except json.JSONDecodeError:
            return {"error": "Failed to parse response from OpenAI", "raw": reply}

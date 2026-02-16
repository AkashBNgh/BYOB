import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from db_manager import get_schema_representation

load_dotenv()

api_key = os.getenv("HF_API_TOKEN")

if not api_key:
    raise RuntimeError("HF_API_TOKEN not found in environment")

client = InferenceClient(token=api_key)

def natural_language_to_sql(user_question):
    schema = get_schema_representation()

    try:
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert data analyst. Return ONLY a valid SQL SELECT query. No explanation."
                },
                {
                    "role": "user",
                    "content": f"""
Database Schema:
{schema}

Question:
{user_question}
"""
                }
            ],
            temperature=0.2,
            max_tokens=200
        )

        sql = response.choices[0].message.content.strip()

        # 🚧 Guardrail
        sql = response.choices[0].message.content.strip()

        # Remove markdown formatting if present
        if sql.startswith("```"):
            sql = sql.replace("```sql", "").replace("```", "").strip()

        # 🚧 Guardrail
        if not sql.lower().startswith("select"):
            raise ValueError(f"LLM did not return SQL: {sql}")


        return sql

    except Exception as e:
        raise RuntimeError(f"HuggingFace NLP failed: {e}")

import os
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.groq_api_key)

def generate_sql(prompt: str) -> str:
    """
    Sends the prompt to Groq API and returns the generated SQL.
    """
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a precise SQL code generator."},
            {"role": "user", "content": prompt}
        ],
        model="qwen/qwen3-32b",  # Updated to requested Qwen model
        temperature=0.0
    )
    
    generated_text = response.choices[0].message.content.strip()
    return generated_text

"""
Text summarization tool using GPT-4.
"""
import openai
from typing import Dict

def summarize_text(text: str, max_words: int = 100) -> Dict[str, str]:
    """Summarize text using GPT-4."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that creates clear, concise summaries."
                },
                {
                    "role": "user",
                    "content": f"Please summarize this text in {max_words} words or less: {text}"
                }
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        return {
            "summary": response.choices[0].message.content.strip(),
            "status": "success"
        }
        
    except Exception as e:
        return {
            "summary": "",
            "status": "error",
            "error": str(e)
        } 
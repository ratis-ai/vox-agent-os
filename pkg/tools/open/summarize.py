"""
Text summarization tool using GPT-4.
"""
import openai
from typing import Dict

def summarize_text(text: str, max_words: int = 300) -> Dict[str, str]:
    """Summarize text using GPT-4."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that creates clear, concise summaries. "
                        "Focus on the key points and main ideas."
                    )
                },
                {
                    "role": "user",
                    "content": f"Please summarize this text in {max_words} words or less:\n\n{text}"
                }
            ],
            temperature=0.7,
            max_tokens=500
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
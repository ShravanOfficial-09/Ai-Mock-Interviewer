import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENROUTER_API_KEY")

def generate_question(domain, difficulty="medium"):
    prompt = f"""
    You are an AI interview question generator.
    Generate a {difficulty} level interview question for the {domain} domain.
    Only return the question without any extra text.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )

    question = response.choices[0].message.content.strip()
    return question

if __name__ == "__main__":
    print(generate_question("Python", "easy"))


import os
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

@dataclass
class QuestionConfig:
    model: str = "gemini-pro"  # Ensure the correct model name is used

class QuestionGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model_name = "gemini-pro"  # Using the correct model name
        self.local_questions = self._load_question_bank()

    def _load_question_bank(self) -> Dict[str, Dict[str, List[str]]]:
        return {
            "Python": {
                "easy": [
                    "What are Python's built-in data types?",
                    "How do you create a virtual environment?",
                    "Explain the difference between list and tuple."
                ],
                "medium": [
                    "How does Python's garbage collection work?",
                    "Explain decorators with an example.",
                    "What are context managers and how to use them?"
                ],
                "hard": [
                    "Explain the GIL and its impact on multithreading.",
                    "How would you implement a memory-efficient data pipeline?",
                    "Design a metaclass that logs all attribute access."
                ]
            }
        }

    def generate_question(self, domain: str, difficulty: str, context: Optional[str] = None) -> str:
        try:
            if context:
                return self._generate_followup_question(domain, difficulty, context)
            return self._generate_initial_question(domain, difficulty)
        except Exception as e:
            logger.error(f"❌ Failed to generate question: {str(e)}")
            return self._get_fallback_question(domain, difficulty)

    def _generate_initial_question(self, domain: str, difficulty: str) -> str:
        prompt = f"""
        Generate a {difficulty} level technical interview question about {domain}.
        Requirements:
        1. Must test practical, hands-on knowledge
        2. Should be answerable in 2-5 minutes
        3. No theoretical definitions
        4. Format: Just the question, no numbering or prefixes
        """

        try:
            # Using the correct method to generate text from the Gemini model
            response = genai.generate_text(model=self.model_name, prompt=prompt)
            question = response.text.strip()
            if self._validate_question(question):
                return question
        except Exception as e:
            logger.warning(f"⚠️ Gemini API failed: {str(e)}")

        return self._get_local_question(domain, difficulty)

    def _generate_followup_question(self, domain: str, difficulty: str, context: str) -> str:
        prompt = f"""
        Based on this interview context, generate a {difficulty} level follow-up question about {domain}:

        Previous Discussion:
        {context}

        Requirements:
        1. Must logically follow from the context
        2. Should probe deeper into the topic
        3. Must be technically specific
        4. Format: Just the question, no prefixes
        """

        try:
            response = genai.generate_text(model=self.model_name, prompt=prompt)
            question = response.text.strip()
            if self._validate_question(question):
                return question
        except Exception as e:
            logger.warning(f"⚠️ Gemini follow-up failed: {str(e)}")

        return self._get_local_followup(domain, difficulty)

    def _validate_question(self, question: str) -> bool:
        return (
            len(question) > 10 and 
            len(question) < 250 and
            any(c.isalpha() for c in question) and
            not question.startswith(("I'm sorry", "As an AI"))
        )

    def _get_local_question(self, domain: str, difficulty: str) -> str:
        domain_questions = self.local_questions.get(domain, {})
        questions = domain_questions.get(difficulty, []) or \
                    domain_questions.get("medium", []) or \
                    domain_questions.get("hard", []) or \
                    domain_questions.get("easy", [])
        return random.choice(questions) if questions else f"Explain a challenging {domain} problem you've solved."

    def _get_fallback_question(self, domain: str, difficulty: str) -> str:
        return self._get_local_question(domain, difficulty)

    def _get_local_followup(self, domain: str, difficulty: str) -> str:
        return f"Can you elaborate more on your approach in {domain}?"

import os

from dotenv import load_dotenv
from groq import Groq

from karmapash.providers.base import LLMProvider


load_dotenv()


class GroqProvider(LLMProvider):

    def __init__(self, model: str = "openai/gpt-oss-20b"):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set in the environment."
            )

        self.client = Groq(api_key=api_key)
        self.model = model

    def chat(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content
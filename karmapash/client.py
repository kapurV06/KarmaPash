from karmapash.pipeline import analyze_prompt
from karmapash.providers.base import LLMProvider
from karmapash.providers.groq_provider import GroqProvider

class KarmaPash:
    def __init__(self, provider: LLMProvider | None = None):
        self.provider = provider or GroqProvider()

    def scan(self, prompt: str) -> dict:
        return analyze_prompt(prompt)

    def chat(self, prompt: str) -> dict:
        security_result = self.scan(prompt)

        decision = security_result["policy"]["decision"]

        if decision == "BLOCK":
            return {
                "blocked": True,
                "response": None,
                "security": security_result,
            }

        response = self.provider.chat(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        return {
            "blocked": False,
            "response": response,
            "security": security_result,
        }
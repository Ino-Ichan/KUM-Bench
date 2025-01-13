import os

import google.generativeai as genai
import openai

OPENAI_MODEL_NAMES = [
    "gpt-4o",
    "gpt-4o-2024-11-20",
    "gpt-4o-mini",
    "o1",
    "o1-preview",
    "o1-mini",
]

GEMINI_MODEL_NAMES = [
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-2.0-flash-thinking-exp-1219",
]


class OpenAIModel:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = openai.OpenAI()

    def generate(self, prompt: str, temperature: float = 0.0, n_generations: int = 1):
        if "o1" in self.model_name:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
            )
        else:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                n=n_generations,
            )
        if n_generations > 1:
            return [choice.message.content for choice in response.choices]
        else:
            return response.choices[0].message.content


class GeminiModel:
    def __init__(self, model_name: str):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.client = genai.GenerativeModel(model_name)

    def generate(self, prompt: str, temperature: float = 0.0, n_generations: int = 1):
        generation_config = genai.GenerationConfig(
            temperature=temperature,
        )
        response = self.client.generate_content(
            prompt, generation_config=generation_config
        )
        try:
            return response.text
        except Exception as e:
            print(f"Error: {e}")
            return ""

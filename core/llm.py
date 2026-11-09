import json
import re
import litellm
from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()                  # reads your .env file
litellm.drop_params = True     # ignore settings a model doesn't support
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")


import time

# Optional backup model, used if the main one keeps failing
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL")


def ask_llm(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
    """Send a message to the AI. Retries on temporary errors."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    models = [MODEL] + ([FALLBACK_MODEL] if FALLBACK_MODEL else [])

    last_error = None
    for model in models:
        for attempt in range(4):  # try up to 4 times per model
            try:
                response = completion(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                )
                return response.choices[0].message.content
            except (litellm.ServiceUnavailableError,
                    litellm.RateLimitError,
                    litellm.InternalServerError) as e:
                last_error = e
                time.sleep(2 ** attempt)  # wait 1s, 2s, 4s, 8s
    raise last_error


def ask_json(system_prompt: str, user_prompt: str, schema):
    """Ask the AI to reply in a strict JSON format, then check it with pydantic."""
    rules = (
        "\n\nReply with ONLY valid JSON matching this schema. "
        "No explanation, no markdown.\n" + json.dumps(schema.model_json_schema())
    )
    raw = ask_llm(system_prompt, user_prompt + rules)
    raw = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    return schema.model_validate_json(raw)
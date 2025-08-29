import json, time
from openai import OpenAI
from ..core.config import MODEL_NAME, TEMPERATURE

_client = OpenAI()  # reads env key

SYSTEM = (
    "You extract structured data from a candidate resume and a job description. "
    "Output STRICT JSON only (no markdown). Keys: skills:list[str] (8-15 items, lowercase nouns), "
    "score:int 0-100, reasons:str (<120 words)."
)

def call_model(user_prompt: str, model_override: str = None, temp_override: float = None, attempts: int = 3, delay: float = 0.8) -> dict:
    last = None
    for i in range(attempts):
        try:
            resp = _client.chat.completions.create(
                model=model_override or MODEL_NAME,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temp_override if temp_override is not None else TEMPERATURE,
            )
            raw = resp.choices[0].message.content.strip()
            return json.loads(raw)
        except Exception as e:
            last = e
            if i < attempts - 1:
                time.sleep(delay)
    raise last

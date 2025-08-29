from .llm import call_model

def build_prompt(resume_text: str, job_text: str) -> str:
    return (
        f"Resume:\n{resume_text}\n\nJob:\n{job_text}\n\n"
        'Return JSON ONLY like: {"skills":["..."],"score":87,"reasons":"..."}'
    )

def parse_resume_job(resume_text: str, job_text: str, model: str = None, temperature: float = None) -> dict:
    prompt = build_prompt(resume_text, job_text)
    return call_model(prompt, model_override=model, temp_override=temperature)

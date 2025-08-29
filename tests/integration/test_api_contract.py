import json, requests, os, pytest

API = os.getenv("API_URL", "http://127.0.0.1:8001")

@pytest.mark.integration
def test_health():
    r = requests.get(f"{API}/health", timeout=10)
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

@pytest.mark.integration
def test_parse_sample():
    resume = "Experienced Python dev with FastAPI and OpenAI."
    job = "Need AI engineer to build a resume parser using Python and FastAPI."
    r = requests.post(f"{API}/parse", json={"resume_text": resume, "job_text": job}, timeout=30)
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body["skills"], list)
    assert 0 <= body["score"] <= 100
    assert isinstance(body["reasons"], str)

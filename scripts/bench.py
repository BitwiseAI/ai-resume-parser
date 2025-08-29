import time, requests, os, json

API = os.getenv("API_URL", "http://127.0.0.1:8000")
AUTH = os.getenv("AUTH_TOKEN", "my-demo-password")
H = {"Authorization": f"Bearer {AUTH}"} if AUTH else {}

resume = "Python dev with FastAPI and OpenAI."
job = "Need AI engineer with FastAPI."
N = 10
lat = []

print(f"Benchmarking against {API}...")

for i in range(N):
    print(f"Run {i+1}/{N}...")
    t = time.time()
    try:
        r = requests.post(f"{API}/parse", json={"resume_text": resume, "job_text": job}, headers=H, timeout=60)
        r.raise_for_status()
        lat.append(time.time() - t)
    except requests.exceptions.RequestException as e:
        print(f"  Error: {e}")
        break

if lat:
    print("\n--- Results ---")
    print(f"runs: {len(lat)}\navg_sec: {sum(lat)/len(lat):.2f}\nmin: {min(lat):.2f}\nmax: {max(lat):.2f}")
    print("\n--- Sample Response ---")
    print(json.dumps(r.json(), indent=2))

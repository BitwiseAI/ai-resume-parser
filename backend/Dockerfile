# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app

# Copy requirements that live in backend/
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY app /app/app

# (We do NOT copy ../data; on Render you'll attach a /data disk)
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

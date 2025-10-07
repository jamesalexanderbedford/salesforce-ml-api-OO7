FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt
COPY api.py model.joblib model_config.json ./
EXPOSE 8000
CMD sh -c 'uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}'

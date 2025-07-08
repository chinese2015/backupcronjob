FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backup_cosmosdb.py ./
CMD ["python", "backup_cosmosdb.py"] 
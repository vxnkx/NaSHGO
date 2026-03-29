FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source
COPY src/ ./src/
COPY run.py .
COPY config.example.yaml .
COPY data/ ./data/

# Create output dirs
RUN mkdir -p output reports

CMD ["python", "run.py"]

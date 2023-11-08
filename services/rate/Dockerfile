FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /rate

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/rate .

CMD ["python", "main.py"]
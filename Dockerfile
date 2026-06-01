# Build
FROM python:3-slim AS builder

WORKDIR /code

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final
FROM python:3-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--debug"]
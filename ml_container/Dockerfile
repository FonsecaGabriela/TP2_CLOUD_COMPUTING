FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt /app/
COPY generate_rules.py /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "generate_rules.py"]


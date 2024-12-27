FROM python:3.9-slim-bullseye

WORKDIR /app

COPY app.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 52020

CMD ["python", "app.py", "--host=0.0.0.0"]


FROM python:3.9.23-slim-bookworm
WORKDIR /app
COPY polybot/requirements.txt .
RUN pip install -r polybot/requirements.txt
COPY . .
WORKDIR /app/polybot
CMD ["python", "app.py"]

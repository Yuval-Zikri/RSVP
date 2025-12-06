FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make entrypoint executable
RUN chmod +x scripts/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["./scripts/entrypoint.sh"]

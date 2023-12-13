FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV OUTPUT_DIR=/app/output

CMD ["python", "./export_beamer.py", "--output-dir", "${OUTPUT_DIR}"]
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y gcc && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]

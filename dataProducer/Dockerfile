FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x finnhub/priceProducer.py
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8001

CMD ["python","finnhub/priceProducer.py"]

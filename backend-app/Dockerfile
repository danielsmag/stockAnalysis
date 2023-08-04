FROM python:3.9

WORKDIR /app

ADD . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade flask-sqlalchemy

EXPOSE 6000

# Set environment varibles
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=6000
ENV FLASK_DEBUG=1
ENV PS_DATABSE_URL = "postgresql+psycopg2://airflow:airflow@130.185.119.119/backend-app"
ENV CELERY_BROKER_URL=redis://redis:6379/2
ENV CELERY_RESULT_BACKEND=redis://redis:6379/2
# Run app.py when the container launches
# CMD ["python", "create_db.py"]
CMD ["flask", "run"]
# CMD ["gunicorn", "-b", "0.0.0.0:6000", "run:app"]
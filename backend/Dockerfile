FROM python:3-slim
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt
COPY foodgram/. .
# CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
CMD python3 manage.py runserver 0.0.0.0:8000

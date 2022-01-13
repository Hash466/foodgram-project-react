FROM python:slim
WORKDIR /code
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt
COPY foodgram/. .
CMD python3 manage.py collectstatic --no-input && \
    gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000

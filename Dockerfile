FROM python:3.10.7

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8013

CMD bash -c "python manage.py migrate --noinput && \
    if [ \"$USE_S3\" = \"False\" ] || [ \"$USE_S3\" = \"false\" ]; then \
        python manage.py collectstatic --noinput; \
    else \
        echo 'Skipping collectstatic (USE_S3=True - static files served from S3/MinIO)'; \
    fi && \
    gunicorn --bind 0.0.0.0:8013 school_chale_hum.wsgi"
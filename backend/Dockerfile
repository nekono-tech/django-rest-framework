FROM python:3

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8888", "config.wsgi:application"]

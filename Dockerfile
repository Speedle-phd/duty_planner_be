FROM python:3.13.3-alpine

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r /requirements.txt

COPY . .

EXPOSE 8080

CMD [ "gunicorn","--config", "gunicorn_config.py", "app:app"]
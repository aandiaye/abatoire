FROM tiangolo/uwsgi-nginx:python3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 3000

CMD  ["python3", "app.py"]
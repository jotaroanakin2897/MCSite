FROM python:3.8.2-alpine

WORKDIR /app

ADD . /app

RUN pip --no-cache-dir install -r requirements.txt

CMD ["python","run.py"]
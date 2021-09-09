FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY djBot /app
COPY requirements.txt /app
COPY entrypoint.sh /app
COPY async_upload.py /app
COPY urls.json /app

EXPOSE 8000

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
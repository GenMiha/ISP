FROM python:3.8

RUN mkdir -p /ISP/lab1
WORKDIR /ISP/lab1

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]
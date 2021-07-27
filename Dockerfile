FROM python:3.8-alpine

WORKDIR /app

RUN pip install -U pip

COPY . .

CMD ["python3",  "linux.py"]
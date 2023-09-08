FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

RUN apt-get update
RUN pip install -r /app/requirements.txt
RUN pip install "uvicorn[standard]"

EXPOSE 5000

CMD ["uvicorn"]

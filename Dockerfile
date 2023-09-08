FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

RUN apt-get update
RUN pip install -r /app/requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]

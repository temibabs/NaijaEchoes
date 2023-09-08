FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

RUN apt-get update
RUN pip install -r /app/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]

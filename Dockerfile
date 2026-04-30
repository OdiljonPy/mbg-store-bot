FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /mbg_store_bot

WORKDIR /mbg_store_bot

ADD . /mbg_store_bot/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]

FROM python:3.8

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN rm -rf delhaize

RUN pip install -r requirements.txt

CMD python app.py

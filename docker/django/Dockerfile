FROM python:3.6

ENV PYTHONUNBUFFERED 1
RUN mkdir /resizing_images
COPY ./resizing_images /resizing_images/
WORKDIR /resizing_images/

RUN pip install --upgrade pip && pip install -r requirements.txt
FROM python:3.6.3-alpine
RUN mkdir /app
WORKDIR /app
ADD ./requirements.txt /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV PYTHONUNBUFFERED 1
ADD . /app/
FROM z4inode/telegram-bot:2.0.0
RUN mkdir /src
RUN mkdir /cfg
WORKDIR /src
ADD ./requirements.txt /src/
RUN apk add --update \
    build-base \
    && rm -rf /var/cache/apk/*
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV PYTHONUNBUFFERED 1
ADD ./src /src/src
ADD ./run.py /src/
ADD ./cfg /cfg/
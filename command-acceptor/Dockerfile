FROM z4inode/telegram-bot:2.0.0
RUN mkdir /app
WORKDIR /app
ADD ./requirements.txt /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV PYTHONUNBUFFERED 1
ADD . /app/
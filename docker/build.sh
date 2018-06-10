#/bin/sh

# Telegram-pusher

# Remove models if the left after previous run
rm -rf ../telegram-pusher/shared

# Copy models to the right directory
cp -r ../shared ../telegram-pusher

# command-acceptor

# command-processor

docker-compose build

rm -rf ../telegram-pusher/shared
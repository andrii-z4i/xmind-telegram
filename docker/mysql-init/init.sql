CREATE DATABASE IF NOT EXISTS badmessages;

CREATE TABLE IF NOT EXISTS messages (
  message TEXT,
  time DATETIME
);
GRANT ALL PRIVILEGES ON badmessages.* TO 'test'@'%' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON badmessages.* TO 'test'@'localhost' IDENTIFIED BY 'test';

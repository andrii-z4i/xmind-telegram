How to run functests
---------------

From root folder install packages required for tests

```
pip install -r functests\requirements.txt
```

Run 
```
docker-compose up
```

Run tests 

```
python -m unittest discover functests/telegram-pusher -p *Tests.py -s functests
```
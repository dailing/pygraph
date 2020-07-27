from python:3.8-slim

RUN pip install jupyterlab flask flask-restful peewee redis pandas \
                tqdm cython flask-socketio eventlet gevent gevent-websocket


RUN groupadd -g 1000 d && useradd -g 1000 -m d
USER d

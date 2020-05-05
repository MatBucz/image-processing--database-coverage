FROM jjanzic/docker-python3-opencv

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
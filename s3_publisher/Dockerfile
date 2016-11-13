FROM python:3.5.2
RUN pip install --upgrade pip
RUN pip install boto3
RUN pip install exifread
RUN pip install gevent
RUN pip install huey
RUN pip install pymongo
RUN pip install redis
RUN pip install requests


RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

WORKDIR /opt/photo_extractor
COPY *.py ./

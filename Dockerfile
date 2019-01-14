FROM python:3.7-stretch

RUN pip install kafka-python pymongo

RUN mkdir /indexupdater
WORKDIR /indexupdater

COPY indexdao indexdao
COPY pagedetailsdao pagedetailsdao
COPY urlsource urlsource
COPY PageDetails.py PageDetails.py

COPY main.py main.py

ENV KAFKA_BOOTSTRAP_SERVERS kafka:9092
ENV KAFKA_PAGEDETAILS_TOPIC pagedetails
ENV KAFKA_PAGEDETAILS_GROUP_ID indexupdater

ENV MONGODB_HOST mongo
ENV MONGODB_DB default
ENV MONGODB_PAGEDETAILS_COLLECTION pagedetails
ENV MONGODB_ORTSINDEX_COLLECTION locationindex
ENV MONGODB_ZEITINDEX_COLLECTION timeindex

ENV MONGODB_USERNAME genericparser
ENV MONGODB_PASSWORD genericparser

ENV DEBUG true

CMD ["python3", "-u", "main.py"]

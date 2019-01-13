import os

from indexdao import OrtsIndexDao, ZeitIndexDao
from pagedetailsdao import MongoDBPageDetailsDao
from urlsource import KafkaSource


def env(key):
    value = os.environ.get(key)
    if not value:
        raise Exception(f"environment variable {key} not set!")
    return value

debug = env("DEBUG")

urlSource = KafkaSource({
    "topic": env("KAFKA_PAGEDETAILS_TOPIC"),
    "bootstrap_servers": env("KAFKA_BOOTSTRAP_SERVERS"),
    "group_id": env("KAFKA_PAGEDETAILS_GROUP_ID"),
    "auto_offset_reset": "earliest"
})

pagedetailsdao = MongoDBPageDetailsDao({
    "host": env("MONGODB_HOST"),
    "db": env("MONGODB_DB"),
    "pagedetails_collection": env("MONGODB_PAGEDETAILS_COLLECTION"),
    "username": env("MONGODB_USERNAME"),
    "password": env("MONGODB_PASSWORD"),
    "authSource": env("MONGODB_DB")
})

ortsindexdao = OrtsIndexDao({
    "host": env("MONGODB_HOST"),
    "db": env("MONGODB_DB"),
    "ortsindex_collection": env("MONGODB_ORTSINDEX_COLLECTION"),
    "username": env("MONGODB_USERNAME"),
    "password": env("MONGODB_PASSWORD"),
    "authSource": env("MONGODB_DB")
})

zeitindexdao = ZeitIndexDao({
    "host": env("MONGODB_HOST"),
    "db": env("MONGODB_DB"),
    "zeitindex_collection": env("MONGODB_ZEITINDEX_COLLECTION"),
    "username": env("MONGODB_USERNAME"),
    "password": env("MONGODB_PASSWORD"),
    "authSource": env("MONGODB_DB")
})

while True:
    url = urlSource.getURL()

    if debug:
        print(f"Got url {url}.")

    pagedetails = pagedetailsdao.getPageDetails(url)

    ortsindexdao.updateIndex(pagedetails)
    if debug:
        print(f"Updated index entry {pagedetails.location} for url {url}.")

    zeitindexdao.updateIndex(pagedetails)
    if debug:
        print(f"Updated index entry {pagedetails.date} for url {url}.")
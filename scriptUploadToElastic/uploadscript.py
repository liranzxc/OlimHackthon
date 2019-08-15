
import slate3k as slate
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import uuid
import re



index = 'olim'
type = 'doc'


def readPDF(filename):
    with open(filename, 'rb') as f:
        extracted_text = slate.PDF(f)
    text = extracted_text.text(False)
    text = re.split('\s{4,}', text)
    text = list(map(lambda item: item.replace('\n',' '),text))
    json_list = []
    for p in text:
        if filter_text(p):
            reversed_p = p[::-1]
            json_list.append(create_json(filename, reversed_p, "Dummy_url", datetime.now()))
    return json_list



def indexer(item, index, type):
    print(item)
    item["_type"] = type
    item["_index"] = index
    return item

def filter_text(text):
    min_length = 40
    if len(text) > min_length:
        return True
    return False


def create_json(filename, paragraph, url, timestamp):
    my_map = {

        "Filename": filename,
        "Paragraph": paragraph,
        "URL": url,
        "timestamp": timestamp.__str__(),
        "_id": str(uuid.uuid1())
    }

    return my_map


if __name__ == '__main__':
    path = '2.pdf'
    es = Elasticsearch()
    es.indices.create(index=index, ignore=400)
    print("ok")
    json_list = readPDF(path)
    json_list = list(map(lambda item: indexer(item, index, type),json_list))
    res2 = helpers.bulk(es, json_list, chunk_size=500, request_timeout=200)
    print(res2)
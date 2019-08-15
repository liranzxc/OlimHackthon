
import slate3k as slate
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import uuid
import re

index = 'olim'
search_type = 'doc'
min_paragraph_length = 40


def read_pdf(filename):
    with open(filename, 'rb') as f:
        extracted_text = slate.PDF(f)
    text = extracted_text.text(False)
    text = re.split('\s{4,}', text)
    text = list(map(lambda item: item.replace('\n',' '),text))
    json_list = []
    for p in text:
        if is_long_enough(p):
            reversed_p = p[::-1]
            json_list.append(create_json(filename, reversed_p, "Dummy_url", datetime.now()))
    return json_list


def indexer(item, _index, _type):
    item["_type"] = _type
    item["_index"] = _index
    return item


def is_long_enough(text):
    if len(text) > min_paragraph_length:
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
    json_list = []
    for i in range(1, 10):
        print("reading file num " + str(i))
        path = 'examples/' + str(i) + '.pdf'
        json_list.extend(read_pdf(path))

    es = Elasticsearch()
    es.indices.create(index=index, ignore=400)
    print("ok")
    json_list = list(map(lambda item: indexer(item, index, search_type), json_list))
    res2 = helpers.bulk(es, json_list, chunk_size=500, request_timeout=200)
    print(res2)
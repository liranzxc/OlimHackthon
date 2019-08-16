
import slate3k as slate
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import uuid
import re

index = 'olim'
search_type = 'doc'
min_paragraph_length = 40


def read_pdf(filename, url="pdf"):
    with open(filename, 'rb') as f:
        extracted_text = slate.PDF(f)
    text = extracted_text.text(False)
    return text_to_json(text, url, filename)


def text_to_json(text, src_string, filename, reverse_text=True):
    text = re.split('\s{4,}', text)
    text = list(map(lambda item: item.replace('\n', ' '), text))
    json_list = []
    for p in text:
        if is_long_enough(p):
            if reverse_text:
                p = p[::-1]
            json_list.append(create_json(filename, p, src_string, datetime.now()))
    return json_list


def indexer(item, _index, _type):
    print(item)
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


def upload_json_to_elastic(json_list):
    es = Elasticsearch()
    es.indices.create(index=index, ignore=400)
    json_list = list(map(lambda item: indexer(item, index, search_type), json_list))
    helpers.bulk(es, json_list, chunk_size=500, request_timeout=200)


if __name__ == '__main__':
    json_list = []
    for i in range(1, 10):
        path = 'examples/' + str(i) + '.pdf'
        print("reading file num " + path)
        json_list.extend(read_pdf(path))
    upload_json_to_elastic(json_list)

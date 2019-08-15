
import slate3k as slate
import json
from datetime import datetime
#from elasticsearch import Elasticsearch
#from elasticsearch import helpers

def readPDF(filename):
    with open(filename, 'rb') as f:
        extracted_text = slate.PDF(f)
    text = extracted_text.text(False)
    text = text.split("\n\n")
    json_list = []
    for p in text:
        if filter_text(p):
            reversed_p = p[::-1]
            #print(reversed_p)
            json_list.append(create_json(filename, reversed_p, "Dummy_url", datetime.now()))
    return json_list


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
        "_index": "olim",
        "_type": "doc"
    }

    json_text = json.dumps(my_map)
    return json_text


if __name__ == '__main__':
    path = '2.pdf'
#    es = Elasticsearch()
    json_list = readPDF(path)
    print(json_list)
    print(len(json_list))
    #helpers.bulk(es, json_list)

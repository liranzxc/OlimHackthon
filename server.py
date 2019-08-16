from flask import Flask, request, jsonify
from datetime import datetime
from elasticsearch import Elasticsearch
from TranslateAPI import Translation
app = Flask(__name__)


def SearchElastic(desc):
    desc = desc[::-1]
    body = {"query": {
        "multi_match": {
            "query": "*"+str(desc)+"*",
            "fuzziness": "auto"
        }
    }}
    res = es.search(index="olim", body=body)
    total = res["hits"]["total"]["value"]
    if total > 0:
        return res["hits"]["hits"]
    else:
        return {}


def flip(item):
    if item["_source"]["URL"] == 'pdf':
        return {'text' : item["_source"]["Paragraph"][::-1] ,'url':item["_source"]["URL"] }
    else:
        return {"text" : item["_source"]["Paragraph"] ,'url':item["_source"]["URL"] }

def trasHeb(item,target):
    item["text"] =  Translation.translate_from_hebrew_to_target(item["text"], target)
    return item


@app.route("/", methods=['POST'])
def SearchResults():
    if request.method == 'POST':
        data = request.json
        desc = data["desc"]
        desc = desc[::-1]
        target = data["len"]

        lendic = Translation.lenguages().values()
        if target not in lendic:
            return {"err": "len not supported yet !"}

        hebrew = Translation.translate_to_hebrew(desc)
        results = SearchElastic(hebrew)

        results = list(map(flip,results ))

        finalResult = []
        for r in results:
            finalResult.append(trasHeb(r,target))

        if len(finalResult) > 0:
            return jsonify({"data" : finalResult})
        else:
            return jsonify({"data": {}})


if __name__ == "__main__":
    es = Elasticsearch()
    app.run(host="0.0.0.0")

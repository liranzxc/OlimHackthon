from flask import Flask, request, jsonify
from datetime import datetime
from elasticsearch import Elasticsearch
from TranslateAPI import Translation
app = Flask(__name__)


def SearchElastic(desc):
    desc = desc[::-1]
    body = {"query": {
        "multi_match": {
            "query": desc,
            "fuzziness": "auto"
        }
    }}
    res = es.search(index="olim", body=body)
    total = res["hits"]["total"]["value"]
    if total > 0:
        return res["hits"]["hits"][0]["_source"]
    else:
        return {}


@app.route("/", methods=['POST'])
def SearchResults():
    if request.method == 'POST':
        data = request.json
        desc = data["desc"]
        target = data["len"]

        lendic = Translation.lenguages().values()
        if target not in lendic:
            return {"err": "len not supported yet !"}

        hebrew = Translation.translate_to_hebrew(desc)
        results = SearchElastic(hebrew)
        if results is not {}:
            neg = Translation.translate_from_hebrew_to_target(results["Paragraph"], target)
            print("neg :" + str(neg))
            return jsonify({"data" : neg})
        else:
            return jsonify({"data": {}})


if __name__ == "__main__":
    es = Elasticsearch()
    app.run(host="0.0.0.0")

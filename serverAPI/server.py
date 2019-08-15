from flask import Flask, request, jsonify
from datetime import datetime
from elasticsearch import Elasticsearch

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
        return jsonify(res["hits"]["hits"][0]["_source"])
    else:
        return {}

@app.route("/", methods=['POST'])
def SearchResults():
    if request.method == 'POST':
        data = request.json
        results = SearchElastic(data["desc"])
        return results


if __name__ == "__main__":
    es = Elasticsearch()
    app.run(host="0.0.0.0")

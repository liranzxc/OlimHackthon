from flask import Flask, request, jsonify
from datetime import datetime
from elasticsearch import Elasticsearch

app = Flask(__name__)


def SearchElastic(desc):
    body = {}
    res = es.search(index="olim", doc_type="doc", body={
    "query": {
        "multi_match": {
            "query": desc,
            "fields": ["subject", "message"]
        }
    })

@app.route("/", methods=['POST'])
def SearchResults():
    if request.method == 'POST':
        es.index(index="my-index", doc_type='test', id=42, body={"any": "data", "timestamp": datetime.now()})
        return jsonify(request.json)

if __name__ == "__main__":
    es = Elasticsearch()
    app.run(host="0.0.0.0")

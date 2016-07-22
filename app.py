from flask import Flask, request, url_for
from elasticsearch import Elasticsearch

es = Elasticsearch()

es.indices.delete(index='index', ignore=400)

mappings = {
  "mappings": {
    "test": {
      "properties": {
        "myCompletion":    {
                    "type": "completion",
                    "analyzer" : "simple",
                    "search_analyzer" : "simple",
                    "preserve_position_increments" : False
        }
      }
    }
  }
}

es.indices.create(index='index', body=mappings, ignore=400)


# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def form():
    return 'funcionou'

@app.route('/entities/', methods=['POST'])
def add():
    title=request.form['title']
    tipo=request.form['tipo']
    new_doc = {
    "title": title,
    "tipo":tipo,
    'myCompletion' : {
        'input' : title.split(" "),
        'output' : title
        }
        }

    res = es.index(index='index', doc_type='test', body=new_doc)
    return str(res)


@app.route('/busca/', methods=['GET'])
def busca():
    q=request.args.get('q')
    print('o valor de q e: ' +q)
    suggest = {
           "please_suggest" : {
                'text' : q,
                "completion" : {
                    "field" : "myCompletion",
                     "fuzzy": True
                }
            }
        }
    res=es.suggest(index='index', body=suggest)['please_suggest']
    return str(res)




# Run the app :)
if __name__ == '__main__':
  app.run(
        host="0.0.0.0",
        port=int("8080")
  )
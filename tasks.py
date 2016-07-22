import celery
from elasticsearch import Elasticsearch

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

es = Elasticsearch()
es.indices.delete(index='index', ignore=400)
es.indices.create(index='index', body=mappings, ignore=400)

app = celery.Celery('tasks')
app.conf.update(BROKER_URL='amqp://guest@localhost//', CELERY_RESULT_BACKEND='rpc://guest@localhost//')
#app.conf.update(BROKER_URL='redis://localhost:6379/0', CELERY_RESULT_BACKEND='redis://localhost:6379/0')


@app.task
def index(title, tipo):
    new_doc = {
    "title": title,
    "tipo": tipo,
    'myCompletion' : {
        'input' : title.split(" "),
        'output' : title
        }
        }
    res = es.index(index='index', doc_type='test', body=new_doc)
    return res

@app.task
def buscar(q):
    suggest = {
           "suggest" : {
                'text' : q,
                "completion" : {
                    "field" : "myCompletion",
                     "fuzzy": True
                }
            }
        }
    res=es.suggest(index='index', body=suggest)
    #['please_suggest']
    return res



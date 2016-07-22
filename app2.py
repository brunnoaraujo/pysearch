from flask import Flask, request, url_for
import tasks

app = Flask(__name__)

@app.route('/')
def form():
    return 'funcionou'

@app.route('/entities/', methods=['POST'])
def add():
    title=request.form['title']
    tipo=request.form['tipo']
    result = tasks.index.delay(title,tipo).get()
    #import pdb;pdb.set_trace()
    #result.wait()
    return str(result)


@app.route('/busca/')
def busca():
    q=request.args.get('q')
    print('o valor de q e: ' +q)
    result = tasks.buscar.delay(q).get()
    #result.wait()
    #import pdb;pdb.set_trace()
    print (result)
    return str(result)




# Run the app :)
if __name__ == '__main__':
  app.run(
        host="0.0.0.0",
        port=int("8080")
  )
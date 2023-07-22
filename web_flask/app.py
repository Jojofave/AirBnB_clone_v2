from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello HBNB!'

@app.route('/hbnb')
def hbnb():
    return 'HBNB'

@app.route('/c/<text>')
def c_text(text):
    text = text.replace('_', ' ')
    return 'C ' + text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


import json

from flask import Flask, render_template

from philogen import PhiloGen

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/gen.json')
def gen():
    generator = PhiloGen()
    return json.dumps(generator.gen(3))

if __name__ == '__main__':
    generator = PhiloGen()
    app.run(debug=True)

import os
import sys
import json
import logging
import datetime
import random

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from philogen import PhiloGen

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Resolution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resolved = db.Column(db.String(500), unique=True)
    score = db.Column(db.Integer)
    created_asof = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_asof = db.Column(db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)
        
    def __init__(self, resolved):
        self.score = 1
        self.resolved = resolved

db.create_all()
generator = PhiloGen()
generator_1 = PhiloGen(1)
generator_3 = PhiloGen(3)


def prune():
    """
    Prune the cached extractions database to keep below 10,000 records,
    the free limit on Heroku.
    """

    num = db.session.query(Resolution.id).count()
    if(num > 9990):
        for resolution in db.session.query(Resolution
                ).order_by(Resolution.score.asc(),Resolution.updated_asof.asc()
                ).limit(40):

            db.session.delete(resolution)
            
    db.session.commit()


def like(resolved):
    if resolved[:3] == "R: ":
        resolved = resolved[3:]

    r = Resolution.query.filter_by(resolved=resolved).first()
    
    if r is not None:
        r.score += 1
    else:
        r = Resolution(resolved)
        
    print "Like {}: {}".format(r.score, r.resolved)
    
    db.session.add(r)
    db.session.commit()
    prune()


# Homepage with randomly generated resolutions
@app.route('/gen.json', methods=['GET', 'POST'])
def gen_json():
    if request.method == 'POST':
        like(request.form.getlist('R')[0])

    resolutions = generator.gen(6)
    resolutions += generator_1.gen(1)
    resolutions += generator_3.gen(1)
    random.shuffle(resolutions)
    return json.dumps(resolutions)

@app.route('/')
def gen():
    return render_template('index.html', url='/gen.json')


# Tournoment page with previously-approved resolutions
@app.route('/tournament.json', methods=['GET', 'POST'])
def tournament_json():
    if request.method == 'POST':
        like(request.form.getlist('R')[0])

    query = db.session.query(Resolution
        ).order_by(func.random()
        ).limit(10)
    resolutions = [r.resolved for r in query]
    return json.dumps(resolutions)

@app.route('/tournament')
def tournament():
    return render_template('index.html', url='/tournament.json')


# Best of all resolutions
@app.route('/best')
def best():
    resolutions = db.session.query(Resolution
        ).order_by(Resolution.score.desc()
        ).limit(500)
    
    return render_template('best.html', resolutions=resolutions)


if __name__ == '__main__':
    app.run(debug=True)

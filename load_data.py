from io import TextIOWrapper
import csv
import pandas as pd
from datetime import datetime
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# Create Flaskk app, config the db and load the db object
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Site(db.Model):
    __tablename__ = 'site'

    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(32), unique=True)
    latitude  = db.Column(db.Float)
    longitude = db.Column(db.Float)
    records   = db.relationship('Record', backref='site')

class Record(db.Model):
    __tablename__ = 'record'

    id             = db.Column(db.Integer, primary_key=True)
    site_id        = db.Column(db.Integer, db.ForeignKey('site.id'))
    temperature    = db.Column(db.Float)
    humidity       = db.Column(db.Float)
    wind_speed     = db.Column(db.Float)
    wind_direction = db.Column(db.Float)
    date_time      = db.Column(db.DateTime)

db.create_all()

df = pd.read_csv("sensors_data.csv")
records_list = []
for index, row in df.iterrows():
    date_time = datetime.strptime(f"{row['date']}:{row['hour']}", ("%Y/%m/%d:%H"))
    site = Site.query.filter_by(name=row['StasName']).first()
    if not site:
        # Create site
        site = Site(name=row['StasName'], latitude=row['Latitude'], longitude=row['Longitude'] )
        db.session.add(site)

    # Add record
    record = Record(site_id=site.id, temperature=row['Temperature'], humidity=row['Humidity'],\
        wind_speed=row['WindSpeed'], wind_direction=row['WindDir'], date_time=date_time)    
    db.session.add(record)

    if index % 1000 == 0:
        print(index)

db.session.commit()

if __name__ == '__main__':
    app.run()
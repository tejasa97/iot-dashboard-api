from app import db
from app.main.exceptions import InvalidSite
from datetime import date

class Site(db.Model):
    __tablename__ = 'site'

    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(32), unique=True)
    latitude  = db.Column(db.Float)
    longitude = db.Column(db.Float)
    records   = db.relationship('Record', backref='site')
    
    @classmethod
    def get_all_sites(self):
        """ Get details of all the sites """
        sites = Site.query.all()

        return sites

    @classmethod
    def get_current_metrics(self, site_name):
        """ Get the latest metrics of a site """
        try:
            site = Site.query.filter_by(name=site_name).first()
            latest_record = Record.query.filter_by(site_id=site.id).order_by(Record.id.desc()).first()
        except:
            raise InvalidSite(site_name)

        return latest_record

class Record(db.Model):
    __tablename__ = 'record'

    id             = db.Column(db.Integer, primary_key=True)
    site_id        = db.Column(db.Integer, db.ForeignKey('site.id'))
    temperature    = db.Column(db.Float)
    humidity       = db.Column(db.Float)
    wind_speed     = db.Column(db.Float)
    wind_direction = db.Column(db.Float)
    date_time      = db.Column(db.DateTime)

from app import db
from app.main.exceptions import InvalidSite
from datetime import date
from sqlalchemy import and_
from sqlalchemy.orm import load_only

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
    def get_current_metrics_records(self, site_name):
        """ Get the latest metrics of a site """
        try:
            site = Site.query.filter_by(name=site_name).first()
            latest_record = Record.query.filter_by(site_id=site.id).order_by(Record.id.desc()).first()
        except:
            raise InvalidSite(site_name)

        return latest_record

    def get_stats_records(self, date_range):

        start_date, end_date = date_range

        records = Record.query.filter_by(site_id=self.id).filter(Record.date_time.between(start_date, end_date)).\
            values('temperature', 'humidity', 'wind_speed', 'wind_direction')

        return records


class Record(db.Model):
    __tablename__ = 'record'

    id             = db.Column(db.Integer, primary_key=True)
    site_id        = db.Column(db.Integer, db.ForeignKey('site.id'))
    temperature    = db.Column(db.Float)
    humidity       = db.Column(db.Float)
    wind_speed     = db.Column(db.Float)
    wind_direction = db.Column(db.Float)
    date_time      = db.Column(db.DateTime)

    @classmethod
    def get_data_site(self, metric, site, date_range):
        """Get the metric values for a date range"""

        start_date, end_date = date_range
        
        # load only required metric
        records = Record.query.filter_by(site_id=site.id).filter(Record.date_time.between(start_date, end_date)).\
            options(load_only(metric, 'date_time')).values(metric, 'date_time')

        return records
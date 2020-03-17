# from app.auth.serializer import UsersSchema
from app.main.models import Site, Record
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields

marsh = Marshmallow()

class SiteSerializer(marsh.Schema):

    class Meta:
        fields = (
            'name',
            'latitude',
            'longitude'
        )

class RecordSerializer(marsh.Schema):
    
    class Meta:
        fields = (
            'temperature',
            'humidity',
            'wind_speed',
            'wind_direction',
            'date_time'
        )
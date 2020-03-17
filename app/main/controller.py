from app import db
from app.main import main_bp
from app.main.exceptions import InvalidSite
from app.main.models import Site, Record
from app.main.serializer import RecordSerializer, SiteSerializer
from flask import jsonify, request, make_response, abort, Response
import json

# All sites
@main_bp.route('/sites')
def sites():
    """Get details of all sites """

    response = {}

    sites = Site.get_all_sites()
    response = SiteSerializer(many=True).dump(sites)

    return Response(json.dumps(response), 
        mimetype='application/json')

# Latest metrics
@main_bp.route('/<string:site_name>/current_metrics')
def current_metrics(site_name):
    """Get the latest metrics for a site """

    response = {}
    
    try:
        latest_metrics = Site.get_current_metrics(site_name)
    except InvalidSite as e:
        abort(400, str(e))

    response = RecordSerializer().dump(latest_metrics)

    return Response(json.dumps(response), 
        mimetype='application/json')

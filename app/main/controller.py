from app import db
from app.main import main_bp
from app.main.exceptions import InvalidSite
from app.main.models import Site, Record
from app.main.serializer import RecordSerializer, SiteSerializer
from datetime import datetime
from flask import jsonify, request, make_response, abort, Response
import json
from operator import itemgetter 

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

@main_bp.route('/<string:site_name>/<string:metric>/')
def get_data(site_name, metric):
    """Get the metric values for a date range  """
    
    response = {}

    site = Site.query.filter_by(name=site_name.upper()).first()
    if site is None:
        abort(400, "Invalid site name")

    start_date_raw = request.args.get("start_date")
    end_date_raw   = request.args.get("end_date")

    if start_date_raw is None or end_date_raw is None:
        abort(400, "Required data not provided")

    try:
        start_date = datetime.strptime(start_date_raw, "%Y-%m-%d")
        end_date   = datetime.strptime(end_date_raw, "%Y-%m-%d")
    except ValueError as e:
        abort(400, "Incorrect date format")

    records                     = Record.get_data_site(metric, site, (start_date, end_date))
    metric_list, date_time_list = list(map(list, zip(*records)))

    response = {
        'date_time' : date_time_list,
        metric      : metric_list
    }

    return Response(json.dumps(response), 
        mimetype='application/json')

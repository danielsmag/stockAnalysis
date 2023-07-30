from flask import Blueprint
from flask_restful import Api
from app.resources.googleTrends_resource import KW_list

google_trends = Blueprint('googleTrends', __name__)
api = Api(google_trends)
api.add_resource(KW_list, '/kw/list')

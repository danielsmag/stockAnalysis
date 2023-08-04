from flask import Blueprint
from flask_restful import Api
from app.resources.googleTrends_resource import KW_list
from app.resources.googleTrends_resource import UpdateData

google_trends = Blueprint('googleTrends', __name__)
api = Api(google_trends)
api.add_resource(KW_list, '/kw/list')
api.add_resource(UpdateData, '/update-all')

from flask import Flask
import os
from app.api.version1.blueprints.googleTrends import google_trends
from app.utils.utils import make_celery

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("PS_DATABSE_URL")
    app.config["CELERY_CONFIG"] = {"broker_url": "redis://redis", "result_backend": "redis://redis"}
    celery = make_celery(app)
    celery.set_default()
    # db.init_app(app)
    app.register_blueprint(google_trends,url_prefix='/googleTrends')
    # app.register_blueprint(post_bp)
    return app ,celery
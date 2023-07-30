from flask import Flask
# from .api.v1.blueprints.user import user_bp
from app.api.version1.blueprints.googleTrends import google_trends
# from .models import db

def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    # db.init_app(app)
    app.register_blueprint(google_trends,url_prefix='/googleTrends')
    # app.register_blueprint(post_bp)
    return app
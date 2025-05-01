from flask import Flask, render_template
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from applications.database import db

load_dotenv()

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from applications.routes import auth_bp, datasets_bp, competitions_bp
    from applications.api import api_blueprint
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(datasets_bp)
    app.register_blueprint(competitions_bp)
    app.register_blueprint(api_blueprint, url_prefix="/api")
    
    # Set up CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    @app.route("/")
    def home():
        return render_template("home.html")
    
    return app
from flask import Flask
from flask_cors import CORS
from app.extensions import db
from app.routes.user_routes import user_bp
from app.routes.portfolio_routes import portfolio_bp
from app.routes.investment_routes import investment_bp

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, supports_credentials=True)
    
    # Configure the app
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
    app.register_blueprint(investment_bp, url_prefix='/investment')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 
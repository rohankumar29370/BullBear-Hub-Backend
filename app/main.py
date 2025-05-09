# from app.cli import run
# run()

from flask import Flask

from app.config import Config
from app.extensions import db
from app.routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix='/user') #Letting the flask application know that there is a blueprint. The url_prefix is a good practice and is a structured way of defining paths.

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)




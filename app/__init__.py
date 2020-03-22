from flask import Flask, jsonify, make_response
from config import Config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db      = SQLAlchemy()
migrate = Migrate()

def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code        = getattr(error, 'code', 500)
        error_description = getattr(error, 'name', '')
        error_message     = getattr(error, 'description', '')
        return make_response(jsonify(
            {
                'error':error_code,
                'message':error_message
            }), error_code
        )

    for errcode in [400, 401, 403, 404, 405, 500]:
        app.errorhandler(errcode)(render_error)

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.secret_key = ".*nobodysguessingthis__"
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import main_bp
    app.register_blueprint(main_bp)
    register_errorhandlers(app)

    return app

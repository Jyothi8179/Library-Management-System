# app/__init__.py
# from flask import Flask, send_from_directory
#
# def create_app():
#     app = Flask(__name__)
#
#     from .books import books_bp
#     from .members import members_bp
#     from .auth import auth_bp
#
#     app.register_blueprint(books_bp, url_prefix='/books')
#     app.register_blueprint(members_bp, url_prefix='/members')
#     app.register_blueprint(auth_bp, url_prefix='/auth')
#
#     # Serve the homepage
#     @app.route('/')
#     def homepage():
#         return send_from_directory('frontend', 'index.html')
#
#     # Serve static files (CSS, JS, etc.) if needed
#     @app.route('/<path:filename>')
#     def static_files(filename):
#         return send_from_directory('frontend', filename)
#
#     return app




from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .books import books_bp
    from .members import members_bp
    from .auth import auth_bp

    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Serve the homepage
    @app.route('/')
    def homepage():
        return send_from_directory('frontend', 'index.html')

        # Serve static files (CSS, JS, etc.) if needed
    @app.route('/<path:filename>')
    def static_files(filename):
        return send_from_directory('frontend', filename)

    with app.app_context():
        db.create_all()

    return app

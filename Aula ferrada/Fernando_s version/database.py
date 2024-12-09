from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_bd(app):

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"

    with app.app_context():
       db.init_app(app)
       db.create_all()
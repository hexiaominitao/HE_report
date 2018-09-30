from . import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class HeInfo(db.Model):
    __tablename__ = "heinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mg_id = db.Column(db.String(11), nullable=False)
    scope_view = db.Column(db.String(500), nullable=False)
    pathology = db.Column(db.String(50), nullable=False)
    cell_c = db.Column(db.String(10), nullable=False)
    cell_p = db.Column(db.Integer, nullable=False)
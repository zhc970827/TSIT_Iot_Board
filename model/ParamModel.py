from sqlalchemy.testing import db


class User(db.Model):
    """用户类"""
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Coulumn(db.String)
    password = db.Coulumn(db.String)
from gino import Gino

db = Gino()


class User(db.Model):
    """用户类"""
    __tablename__ = 'users_message_table'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Coulumn(db.String)
    password = db.Coulumn(db.String)
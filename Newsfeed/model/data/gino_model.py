from db_config.gino_connect import db

class Newsfeed(db.Model):
    __tablename__ = 'newsfeed'
    newsfeed_id = db.Column(db.Integer, primary_key=True, default=lambda: db.Sequence('newsfeed_newsfeed_id_seq').next_value())
    author = db.Column(db.String(45))
    headline = db.Column(db.Text)
    summary = db.Column(db.Text)
    media = db.Column(db.LargeBinary)
    publish_date = db.Column(db.Date)
    category = db.Column(db.Text)
    author_id = db.Column(db.Integer)

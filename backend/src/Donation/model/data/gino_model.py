from db_config.gino_connect import db

class Donation(db.Model):
    __tablename__ = 'donation'
    donation_id = db.Column(db.Integer, primary_key=True, default=lambda: db.Sequence('donation_donation_id_seq').next_value())
    campaign_id = db.Column(db.Integer)
    donator_id = db.Column(db.Integer)
    donation_amount = db.Column(db.Numeric)
    donation_date = db.Column(db.Date)
    message_leaving = db.Column(db.Text)
from database import db

class Episode(db.Model):
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    air_date  = db.Column(db.Date, nullable=False)
    description = db.Column(db.String, nullable=False)

    appearances = db.relationship('Appearance', backref='episode', cascade="all, delete", lazy=True)

class Guest(db.Model):
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)

    appearances = db.relationship('Appearance', backref='guest', cascade="all, delete", lazy=True)

class Appearance(db.Model):
    __tablename__ = 'appearances'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    @staticmethod
    def validate_rating(rating):
        return 1 <= rating <= 5

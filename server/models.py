from database import db
from marshmallow import Schema, fields, validates, ValidationError

# Appearance schema using Marshmallow for serialization and validation
class AppearanceSchema(Schema):
    id = fields.Int(dump_only=True)
    rating = fields.Int(required=True)
    episode_id = fields.Int(required=True)
    guest_id = fields.Int(required=True)

    # Marshmallow validation to ensure rating is between 1 and 5
    @validates('rating')
    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise ValidationError("Rating must be between 1 and 5.")


# Episode model
class Episode(db.Model):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # Adding max length for title
    air_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(500), nullable=False)  # Adding max length for description

    # Relationships: One episode has many appearances, with cascading deletes
    appearances = db.relationship(
        'Appearance', 
        backref='episode', 
        cascade="all, delete-orphan", 
        lazy=True
    )

    # Custom validation for title and description to ensure they are not empty
    @staticmethod
    def validate_title_and_description(title, description):
        if not title or not description:
            raise ValueError("Both title and description are required fields.")


# Guest model
class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Adding max length for name
    bio = db.Column(db.String(500), nullable=False)  # Adding max length for bio

    # Relationships: One guest can have many appearances, with cascading deletes
    appearances = db.relationship(
        'Appearance', 
        backref='guest', 
        cascade="all, delete-orphan", 
        lazy=True
    )

    # Custom validation for name and bio to ensure they are not empty
    @staticmethod
    def validate_name_and_bio(name, bio):
        if not name or not bio:
            raise ValueError("Both name and bio are required fields.")


# Appearance model
class Appearance(db.Model):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id', ondelete='CASCADE'), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Ensuring unique guest-episode combination (guest cannot appear in the same episode twice)
    __table_args__ = (
        db.UniqueConstraint('guest_id', 'episode_id', name='unique_guest_episode'),
    )

    # Relationships
    guest = db.relationship('Guest', backref=db.backref('guest_appearances', lazy=True, cascade="all, delete-orphan"))
    episode = db.relationship('Episode', backref=db.backref('episode_appearances', lazy=True, cascade="all, delete-orphan"))

    # Custom validation for rating to ensure it is between 1 and 5
    @staticmethod
    def validate_rating(rating):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")

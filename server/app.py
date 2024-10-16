from flask import Flask, request, make_response
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from models import Episode, Guest, Appearance
from database import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///podcast.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
migrate = Migrate(app, db)


class EpisodeResource(Resource):
    def get(self, id=None):
        if id:
            episode = Episode.query.get(id)
            if not episode:
                return make_response({"message": "Episode not found"}, 404)
            return make_response(episode_schema.dump(episode), 200)
        episodes = Episode.query.all()
        return make_response(episodes_schema.dump(episodes), 200)

    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')

        new_episode = Episode(title=title, description=description)
        db.session.add(new_episode)
        db.session.commit()

        return make_response(episode_schema.dump(new_episode), 201)

    def patch(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return make_response({"message": "Episode not found"}, 404)
        
        data = request.get_json()
        for key, value in data.items():
            setattr(episode, key, value)

        db.session.commit()
        return make_response(episode_schema.dump(episode), 200)

    def delete(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return make_response({"message": "Episode not found"}, 404)

        db.session.delete(episode)
        db.session.commit()
        return make_response({"message": "Episode deleted successfully"}, 200)

class GuestResource(Resource):
    def get(self, id=None):
        if id:
            guest = Guest.query.get(id)
            if not guest:
                return make_response({"message": "Guest not found"}, 404)
            return make_response(guest_schema.dump(guest), 200)
        guests = Guest.query.all()
        return make_response(guests_schema.dump(guests), 200)

    def post(self):
        data = request.get_json()
        name = data.get('name')
        bio = data.get('bio')

        new_guest = Guest(name=name, bio=bio)
        db.session.add(new_guest)
        db.session.commit()

        return make_response(guest_schema.dump(new_guest), 201)

    def patch(self, id):
        guest = Guest.query.get(id)
        if not guest:
            return make_response({"message": "Guest not found"}, 404)
        
        data = request.get_json()
        for key, value in data.items():
            setattr(guest, key, value)

        db.session.commit()
        return make_response(guest_schema.dump(guest), 200)

    def delete(self, id):
        guest = Guest.query.get(id)
        if not guest:
            return make_response({"message": "Guest not found"}, 404)

        db.session.delete(guest)
        db.session.commit()
        return make_response({"message": "Guest deleted successfully"}, 200)

class AppearanceResource(Resource):
    def get(self, id=None):
        if id:
            appearance = Appearance.query.get(id)
            if not appearance:
                return make_response({"message": "Appearance not found"}, 404)
            return make_response(appearance_schema.dump(appearance), 200)
        appearances = Appearance.query.all()
        return make_response(appearances_schema.dump(appearances), 200)

    def post(self):
        data = request.get_json()
        rating = data.get('rating')
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')

        if not Appearance.validate_rating(rating):
            return make_response({"errors": ["Rating must be between 1 and 5"]}, 400)

        new_appearance = Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)
        db.session.add(new_appearance)
        db.session.commit()

        return make_response(appearance_schema.dump(new_appearance), 201)

    def patch(self, id):
        appearance = Appearance.query.get(id)
        if not appearance:
            return make_response({"message": "Appearance not found"}, 404)
        
        data = request.get_json()
        for key, value in data.items():
            setattr(appearance, key, value)

        db.session.commit()
        return make_response(appearance_schema.dump(appearance), 200)

    def delete(self, id):
        appearance = Appearance.query.get(id)
        if not appearance:
            return make_response({"message": "Appearance not found"}, 404)

        db.session.delete(appearance)
        db.session.commit()
        return make_response({"message": "Appearance deleted successfully"}, 200)

# Routes
api.add_resource(EpisodeResource, '/episodes', '/episodes/<int:id>')
api.add_resource(GuestResource, '/guests', '/guests/<int:id>')
api.add_resource(AppearanceResource, '/appearances', '/appearances/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, make_response
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from models import Episode, Guest, Appearance
from database import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///podcast.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)  # SQLAlchemy for ORM
ma = Marshmallow(app)  # Marshmallow for serialization
api = Api(app)  # Flask-Restful API
migrate = Migrate(app, db)  # Database migration support


class EpisodeResource(Resource):
    """Handles CRUD operations for podcast episodes."""

    def get(self, id=None):
        """
        Retrieve episodes. If an ID is provided, return a specific episode.
        
        :param id: ID of the episode to retrieve (optional)
        :return: JSON representation of the episode(s) or a 404 error if not found
        """
        if id:
            episode = Episode.query.get(id)  # Query for a specific episode by ID
            if not episode:
                return make_response({"message": "Episode not found"}, 404)
            return make_response(episode_schema.dump(episode), 200)

        # Return all episodes if no ID is specified
        episodes = Episode.query.all()
        return make_response(episodes_schema.dump(episodes), 200)

    def post(self):
        """
        Create a new episode with the provided title and description.
        
        :return: JSON representation of the created episode and a 201 status code
        """
        data = request.get_json()  # Get JSON data from the request
        title = data.get('title')
        description = data.get('description')

        new_episode = Episode(title=title, description=description)  # Create a new episode instance
        db.session.add(new_episode)  # Add the new episode to the session
        db.session.commit()  # Commit the changes to the database

        return make_response(episode_schema.dump(new_episode), 201)

    def patch(self, id):
        """
        Update an existing episode by ID with new data provided.
        
        :param id: ID of the episode to update
        :return: JSON representation of the updated episode or a 404 error if not found
        """
        episode = Episode.query.get(id)  # Find the episode by ID
        if not episode:
            return make_response({"message": "Episode not found"}, 404)
        
        data = request.get_json()  # Get the JSON data for updating
        for key, value in data.items():
            setattr(episode, key, value)  # Update episode attributes

        db.session.commit()  # Commit the changes
        return make_response(episode_schema.dump(episode), 200)

    def delete(self, id):
        """
        Delete an existing episode by ID.
        
        :param id: ID of the episode to delete
        :return: Success message or a 404 error if not found
        """
        episode = Episode.query.get(id)  # Find the episode by ID
        if not episode:
            return make_response({"message": "Episode not found"}, 404)

        db.session.delete(episode)  # Delete the episode from the session
        db.session.commit()  # Commit the changes
        return make_response({"message": "Episode deleted successfully"}, 200)


class GuestResource(Resource):
    """Handles CRUD operations for podcast guests."""

    def get(self, id=None):
        """
        Retrieve guests. If an ID is provided, return a specific guest.
        
        :param id: ID of the guest to retrieve (optional)
        :return: JSON representation of the guest(s) or a 404 error if not found
        """
        if id:
            guest = Guest.query.get(id)  # Query for a specific guest by ID
            if not guest:
                return make_response({"message": "Guest not found"}, 404)
            return make_response(guest_schema.dump(guest), 200)

        # Return all guests if no ID is specified
        guests = Guest.query.all()
        return make_response(guests_schema.dump(guests), 200)

    def post(self):
        """
        Create a new guest with the provided name and bio.
        
        :return: JSON representation of the created guest and a 201 status code
        """
        data = request.get_json()  # Get JSON data from the request
        name = data.get('name')
        bio = data.get('bio')

        new_guest = Guest(name=name, bio=bio)  # Create a new guest instance
        db.session.add(new_guest)  # Add the new guest to the session
        db.session.commit()  # Commit the changes to the database

        return make_response(guest_schema.dump(new_guest), 201)

    def patch(self, id):
        """
        Update an existing guest by ID with new data provided.
        
        :param id: ID of the guest to update
        :return: JSON representation of the updated guest or a 404 error if not found
        """
        guest = Guest.query.get(id)  # Find the guest by ID
        if not guest:
            return make_response({"message": "Guest not found"}, 404)
        
        data = request.get_json()  # Get the JSON data for updating
        for key, value in data.items():
            setattr(guest, key, value)  # Update guest attributes

        db.session.commit()  # Commit the changes
        return make_response(guest_schema.dump(guest), 200)

    def delete(self, id):
        """
        Delete an existing guest by ID.
        
        :param id: ID of the guest to delete
        :return: Success message or a 404 error if not found
        """
        guest = Guest.query.get(id)  # Find the guest by ID
        if not guest:
            return make_response({"message": "Guest not found"}, 404)

        db.session.delete(guest)  # Delete the guest from the session
        db.session.commit()  # Commit the changes
        return make_response({"message": "Guest deleted successfully"}, 200)


class AppearanceResource(Resource):
    """Handles CRUD operations for guest appearances on episodes."""

    def get(self, id=None):
        """
        Retrieve appearances. If an ID is provided, return a specific appearance.
        
        :param id: ID of the appearance to retrieve (optional)
        :return: JSON representation of the appearance(s) or a 404 error if not found
        """
        if id:
            appearance = Appearance.query.get(id)  # Query for a specific appearance by ID
            if not appearance:
                return make_response({"message": "Appearance not found"}, 404)
            return make_response(appearance_schema.dump(appearance), 200)

        # Return all appearances if no ID is specified
        appearances = Appearance.query.all()
        return make_response(appearances_schema.dump(appearances), 200)

    def post(self):
        """
        Create a new appearance with the provided rating, episode ID, and guest ID.
        
        :return: JSON representation of the created appearance and a 201 status code
        """
        data = request.get_json()  # Get JSON data from the request
        rating = data.get('rating')
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')

        # Validate the rating before creating a new appearance
        if not Appearance.validate_rating(rating):
            return make_response({"errors": ["Rating must be between 1 and 5"]}, 400)

        new_appearance = Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)  # Create a new appearance instance
        db.session.add(new_appearance)  # Add the new appearance to the session
        db.session.commit()  # Commit the changes to the database

        return make_response(appearance_schema.dump(new_appearance), 201)

    def patch(self, id):
        """
        Update an existing appearance by ID with new data provided.
        
        :param id: ID of the appearance to update
        :return: JSON representation of the updated appearance or a 404 error if not found
        """
        appearance = Appearance.query.get(id)  # Find the appearance by ID
        if not appearance:
            return make_response({"message": "Appearance not found"}, 404)
        
        data = request.get_json()  # Get the JSON data for updating
        for key, value in data.items():
            setattr(appearance, key, value)  # Update appearance attributes

        db.session.commit()  # Commit the changes
        return make_response(appearance_schema.dump(appearance), 200)

    def delete(self, id):
        """
        Delete an existing appearance by ID.
        
        :param id: ID of the appearance to delete
        :return: Success message or a 404 error if not found
        """
        appearance = Appearance.query.get(id)  # Find the appearance by ID
        if not appearance:
            return make_response({"message": "Appearance not found"}, 404)

        db.session.delete(appearance)  # Delete the appearance from the session
        db.session.commit()  # Commit the changes
        return make_response({"message": "Appearance deleted successfully"}, 200)


# Define API routes
api.add_resource(EpisodeResource, '/episodes', '/episodes/<int:id>')
api.add_resource(GuestResource, '/guests', '/guests/<int:id>')
api.add_resource(AppearanceResource, '/appearances', '/appearances/<int:id>')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

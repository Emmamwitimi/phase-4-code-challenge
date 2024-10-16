from app import app, db  # Import the app instance and db
from models import Episode, Guest, Appearance
from faker import Faker
import random

fake = Faker()

def seed_data():
    # Add application context
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create sample episodes
        episodes = []
        for _ in range(5):  # Create 5 sample episodes
            episode = Episode(
                title=fake.sentence(),  # Add a title
                air_date=fake.date(),
                description=fake.paragraph()  # Add a description
            )
            episodes.append(episode)
        
        # Create sample guests
        guests = []
        for _ in range(10):  # Create 10 sample guests
            guest = Guest(name=fake.name(), bio=fake.paragraph())  # Change occupation to bio
            guests.append(guest)

        # Create sample appearances
        appearances = []
        for episode in episodes:
            for guest in random.sample(guests, random.randint(1, 3)):  # Randomly assign 1-3 guests to each episode
                appearance = Appearance(
                    rating=random.randint(1, 5), 
                    episode_id=episode.id, 
                    guest_id=guest.id
                )
                appearances.append(appearance)

        # Add data to session
        db.session.add_all(episodes)
        db.session.add_all(guests)
        db.session.add_all(appearances)

        # Commit session
        db.session.commit()

if __name__ == '__main__':
    seed_data()
    print("Database seeded successfully!")

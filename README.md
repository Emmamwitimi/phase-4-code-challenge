# Podcast API

This is a RESTful API for managing podcast episodes, guests, and their appearances. Built with Flask, Flask-RESTful, and SQLAlchemy, it allows users to perform CRUD operations on podcast data.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Seeding the Database](#seeding-the-database)
- [License](#license)



### Explanation of Sections
- **Project Description**: A brief overview of what the project is about.
- **Installation**: Step-by-step instructions on how to set up the project.
- **Usage**: How to run the application.
- **API Endpoints**: Describes the available endpoints for interacting with the API.
- **Data Models**: Details the structure of the database models.
- **Seeding the Database**: Instructions for populating the database with sample data.
- **License**: A placeholder for the project's license information.

## API Endpoints

### Episodes:
- `GET /episodes`: Retrieve all episodes.
- `GET /episodes/<id>`: Retrieve a specific episode by ID.
- `POST /episodes`: Create a new episode.
- `PATCH /episodes/<id>`: Update an existing episode.
- `DELETE /episodes/<id>`: Delete an episode.

### Guests:
- `GET /guests`: Retrieve all guests.
- `GET /guests/<id>`: Retrieve a specific guest by ID.
- `POST /guests`: Create a new guest.
- `PATCH /guests/<id>`: Update an existing guest.
- `DELETE /guests/<id>`: Delete a guest.

### Appearances:
- `GET /appearances`: Retrieve all appearances.
- `GET /appearances/<id>`: Retrieve a specific appearance by ID.
- `POST /appearances`: Create a new appearance.
- `PATCH /appearances/<id>`: Update an existing appearance.
- `DELETE /appearances/<id>`: Delete an appearance.

## Data Models

### Episode
- `id`: Integer (Primary Key)
- `title`: String (Not Null)
- `air_date`: Date (Not Null)
- `description`: String (Not Null)

### Guest
- `id`: Integer (Primary Key)
- `name`: String (Not Null)
- `bio`: String (Not Null)

### Appearance
- `id`: Integer (Primary Key)
- `rating`: Integer (Not Null, between 1 and 5)
- `episode_id`: Integer (Foreign Key to Episode, Not Null)
- `guest_id`: Integer (Foreign Key to Guest, Not Null)


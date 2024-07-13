from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500), nullable=True)
    genres = db.Column(db.String(120))
    past_shows = []
    upcoming_shows = []
    past_shows_count = 0
    upcoming_shows_count = 0

    def __init__(self, id, name, city, state, address, phone, image_link, facebook_link, website,
                 seeking_talent, seeking_description, genres):
        self.id = id
        self.name = name
        self.city = city
        self.state = state
        self.address = address
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.website = website
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description
        self.genres = genres
        self.past_shows = []
        self.upcoming_shows = []

    class ShowInfo:
        artist_id = int
        artist_name = str
        artist_image_link = str
        start_time = str

        def __init__(self, artist_id, artist_name, artist_image_link, start_time):
            self.artist_id = artist_id
            self.artist_name = artist_name
            self.artist_image_link = artist_image_link
            self.start_time = start_time

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500), nullable=True)
    past_shows = []
    upcoming_shows = []
    past_shows_count = 0
    upcoming_shows_count = 0

    def __init__(self, id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue,
                 seeking_description):
        self.id = id
        self.name = name
        self.city = city
        self.state = state
        self.phone = phone
        self.genres = genres
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.website = website
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description

    class ShowInfo:
        venue_id = int
        venue_name = str
        venue_image_link = str
        start_time = str

        def __init__(self, venue_id, venue_name, venue_image_link, start_time):
            self.venue_id = venue_id
            self.venue_name = venue_name
            self.venue_image_link = venue_image_link
            self.start_time = start_time

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id))
    start_time = db.Column(db.DateTime)

    def __init__(self, id, artist_id, venue_id, start_time):
        self.id = id,
        self.artist_id = artist_id,
        self.venue_id = venue_id,
        self.start_time = start_time

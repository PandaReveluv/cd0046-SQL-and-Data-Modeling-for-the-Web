#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import datetime
import babel
import sqlalchemy
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from sqlalchemy import func, exc

from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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
    past_shows = []
    upcoming_shows = []
    past_shows_count = 0
    upcoming_shows_count = 0

    def __init__(self, id, name, city, state, address, phone, image_link, facebook_link, website,
                 seeking_talent, seeking_description):
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


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    group_by_city_and_state = (Venue.query.with_entities(Venue.city, Venue.state, func.count(Venue.id))
                               .group_by(Venue.city, Venue.state)).all()
    for city, state, count_id in group_by_city_and_state:
        venues_value = (Venue.query
                        .with_entities(Venue.id, Venue.name)
                        .where(Venue.city == city and Venue.state == state).all())
        data.append({"city": city, "state": state, "venues": venues_value})

    app.logger.info("Getting venues info: %s", data)
    return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_value = request.form.get('search_term')
    search_result = (Venue.query.with_entities(Venue.id, Venue.name)
                     .where(Venue.name.like('%' + search_value + '%'))).all()
    response = {"count": len(search_result), "data": search_result}
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    query_result = (Venue.query.with_entities(Venue, Artist, Show)
                    .join(Show, Venue.id == Show.venue_id, full=True)
                    .join(Artist, Artist.id == Show.artist_id, full=True)
                    .where(Venue.id == venue_id).all())
    if len(query_result) == 0:
        return render_template('pages/show_venue.html', venue={})
    # query_result [[Venue, Artist, Show]]
    map_result = {}
    for result in query_result:
        venue = None
        artist = None
        show = None
        show_info = None
        if result[0] is not None:
            venue = Venue(id=result[0].id,
                          name=result[0].name,
                          address=result[0].address,
                          city=result[0].city,
                          state=result[0].state,
                          phone=result[0].phone,
                          website=result[0].website,
                          facebook_link=result[0].facebook_link,
                          seeking_talent=result[0].seeking_talent,
                          seeking_description=result[0].seeking_description,
                          image_link=result[0].image_link)
        if result[1] is not None:
            artist = Artist(id=result[1].id,
                            name=result[1].name,
                            city=result[1].city,
                            state=result[1].state,
                            phone=result[1].phone,
                            genres=result[1].genres,
                            image_link=result[1].image_link,
                            website=result[1].website,
                            facebook_link=result[1].facebook_link,
                            seeking_venue=result[1].seeking_venue,
                            seeking_description=result[1].seeking_description)
        if result[2] is not None:
            show = Show(id=result[2].id,
                        artist_id=result[2].artist_id,
                        venue_id=result[2].venue_id,
                        start_time=result[2].start_time)
        if artist is not None and show is not None:
            show_info = Venue.ShowInfo(artist_id=artist.id,
                                       artist_name=artist.name,
                                       artist_image_link=artist.image_link,
                                       start_time=str(show.start_time))
        if result[0].id in map_result:
            venue = map_result.get(result[0].id)
            if show.start_time < datetime.now():
                venue.past_shows.append(show_info)
                venue.past_shows_count = venue.past_shows_count + 1
            else:
                venue.upcoming_shows.append(show_info)
                venue.upcoming_shows_count = venue.upcoming_shows_count + 1
        else:
            if show_info is not None:
                if show.start_time < datetime.now():
                    venue.past_shows.append(show_info)
                    venue.past_shows_count = venue.past_shows_count + 1
                else:
                    venue.upcoming_shows.append(show_info)
                    venue.upcoming_shows_count = venue.upcoming_shows_count + 1
            map_result.update({venue.id: venue})
    result = list(map_result.values())[0] if map_result.values() is not None else []
    return render_template('pages/show_venue.html', venue=result)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = VenueForm(request.form)
    venue = Venue(id=None,
                  name=form.name.data,
                  address=form.address.data,
                  city=form.city.data,
                  state=form.state.data,
                  phone=form.phone.data,
                  website=form.website_link.data,
                  facebook_link=form.facebook_link.data,
                  seeking_talent=form.seeking_talent.data,
                  seeking_description=form.seeking_description.data,
                  image_link=form.image_link.data)
    try:
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + venue.name + ' was successfully listed!')
    except exc.SQLAlchemyError:
        flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
        db.session.rollback()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        Venue.query.where(Venue.id == venue_id).delete()
        db.session.commit()
        flash('Venue id ' + venue_id + ' was successfully deleted!')
    except exc.SQLAlchemyError:
        flash('An error occurred. Venue id ' + venue_id + ' could not be deleted.')
        db.session.rollback()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = Artist.query.with_entities(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_value = request.form.get('search_term').lower()
    search_result = (Artist.query.with_entities(Artist.id, Artist.name)
                     .where(func.lower(Artist.name).like('%' + search_value + '%'))).all()
    response = {"count": len(search_result), "data": search_result}
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    query_result = (Artist.query.with_entities(Venue, Artist, Show)
                    .join(Show, Artist.id == Show.artist_id, full=True)
                    .join(Venue, Venue.id == Show.venue_id, full=True)
                    .where(Artist.id == artist_id).all())
    if len(query_result) == 0:
        return render_template('pages/show_venue.html', venue={})
    # query_result [[Venue, Artist, Show]]
    map_result = {}
    for result in query_result:
        venue = None
        artist = None
        show = None
        show_info = None
        if result[0] is not None:
            venue = Venue(id=result[0].id,
                          name=result[0].name,
                          address=result[0].address,
                          city=result[0].city,
                          state=result[0].state,
                          phone=result[0].phone,
                          website=result[0].website,
                          facebook_link=result[0].facebook_link,
                          seeking_talent=result[0].seeking_talent,
                          seeking_description=result[0].seeking_description,
                          image_link=result[0].image_link)
        if result[1] is not None:
            artist = Artist(id=result[1].id,
                            name=result[1].name,
                            city=result[1].city,
                            state=result[1].state,
                            phone=result[1].phone,
                            genres=result[1].genres.replace('{', '').replace('}', '').split(','),
                            image_link=result[1].image_link,
                            website=result[1].website,
                            facebook_link=result[1].facebook_link,
                            seeking_venue=result[1].seeking_venue,
                            seeking_description=result[1].seeking_description)
        if result[2] is not None:
            show = Show(id=result[2].id,
                        artist_id=result[2].artist_id,
                        venue_id=result[2].venue_id,
                        start_time=result[2].start_time)
        if artist is not None and show is not None:
            show_info = Artist.ShowInfo(venue_id=venue.id,
                                        venue_name=venue.name,
                                        venue_image_link=venue.image_link,
                                        start_time=str(show.start_time))
        if artist.id in map_result:
            artist = map_result.get(artist.id)
            if show.start_time < datetime.now():
                artist.past_shows.append(show_info)
                artist.past_shows_count = artist.past_shows_count + 1
            else:
                artist.upcoming_shows.append(show_info)
                artist.upcoming_shows_count = artist.upcoming_shows_count + 1
        else:
            if show_info is not None:
                if show.start_time < datetime.now():
                    artist.past_shows.append(show_info)
                    artist.past_shows_count = artist.past_shows_count + 1
                else:
                    artist.upcoming_shows.append(show_info)
                    artist.upcoming_shows_count = artist.upcoming_shows_count + 1
            map_result.update({artist.id: artist})
    result = list(map_result.values())[0] if map_result.values() is not None else []
    return render_template('pages/show_artist.html', artist=result)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = ArtistForm(request.form)
    artist = Artist(id=None,
                    name=form.name.data,
                    city=form.city.data,
                    state=form.state.data,
                    phone=form.phone.data,
                    genres=form.genres.data,
                    website=form.website_link.data,
                    facebook_link=form.facebook_link.data,
                    seeking_venue=form.seeking_venue.data,
                    seeking_description=form.seeking_description.data,
                    image_link=request.form.get('image_link'))
    try:
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except exc.SQLAlchemyError:
        flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
        db.session.rollback()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = (Show.query.with_entities(Venue.id.label("venue_id"),
                                     Venue.name.label("venue_name"),
                                     Artist.id.label("artist_id"),
                                     Artist.name.label("artist_name"),
                                     Artist.image_link.label("artist_image_link"),
                                     func.cast(Show.start_time, sqlalchemy.String).label("start_time"))
            .join(Venue, Show.venue_id == Venue.id)
            .join(Artist, Show.artist_id == Artist.id)
            .all())
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    form = ShowForm(request.form)
    show_id = db.session.execute(sqlalchemy.select(func.next_value(sqlalchemy.Sequence('Show_id_seq')))).first()[0]
    show = Show(id=show_id,
                venue_id=form.venue_id.data,
                artist_id=form.artist_id.data,
                start_time=form.start_time.data)
    try:
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except exc.SQLAlchemyError as e:
        logging.error('Error at creating show: %s', repr(e))
        flash('An error occurred. Show could not be listed.')
        db.session.rollback()
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

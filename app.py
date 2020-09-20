#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy import func
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
# TODO: connect to a local postgresql database ==DONE==

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
    website = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean())
    seeking_talent_description = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    # genres = db.relationship('Genres_of_Venues' ,cascade="all,delete" ,  backref = 'venue')
    shows = db.relationship('Show' ,cascade="all,delete" ,  backref = 'venue')


    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    migrate = Migrate(app, db)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean())
    seeking_venue_description = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    # genres = db.relationship('Genres_of_Artists' , cascade="all,delete"  ,  backref = 'artist')
    shows = db.relationship('Show' ,cascade="all,delete"  ,  backref = 'artist')

  
class Show(db.Model):
  __tablename__ = 'Show' 
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime())
  artist_id = db.Column(db.Integer , db.ForeignKey('Artist.id'))
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  current_date = datetime.now()
  data = []
  cities = Venue.query.with_entities(Venue.city, Venue.state).distinct(Venue.city).all()
  for entry in cities: 
      dic = {}
      dic['city'] = entry[0] 
      dic['state'] = entry[1]
      dic['venues'] = [] 
      query_venues =  Venue.query.with_entities(Venue.id , Venue.name).filter(Venue.city == dic['city']).all()
      for venue_entry in query_venues:
        venue_dic = {}
        venue_dic['id'] = venue_entry[0]
        venue_dic['name'] = venue_entry[1]
        upcoming_shows = Show.query.filter(Show.venue_id == venue_dic['id'] , Show.date > current_date).count() # should it be >= ?? 
        venue_dic['num_upcoming_shows'] = upcoming_shows
        dic['venues'].append(venue_dic)
      print(dic)
      data.append(dic)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []
  for venue in result:
    dic = {
      'id': venue.id,
      'name':venue.name, 
      'num_upcoming_shows':Show.query.filter(Venue.id == venue.id).count()
    }
    data.append(dic)

  response = {
    "count" : len(result),
    "data" : data
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = {}
  venues = Venue.query.filter(Venue.id == venue_id).all()
  # we make a loop so that if the venue is  null it keep the data list empty 
  for v in venues :
      data['id'] = v.id
      data['name'] = v.name
      if(v.genres == None):
        data['genres'] = "" 
      else:
        data['genres'] = v.genres
      data['address'] = v.address
      data['city'] = v.city
      data['state'] = v.state
      data['phone'] = v.phone
      data['website'] = v.website
      data['facebook_link'] = v.facebook_link
      data['seeking_talent'] = v.seeking_talent
      data['seeking_description'] = v.seeking_talent_description
      data['image_link'] = v.image_link
      past_shows = [] 
      upcoming_shows = []
      current_date = datetime.now()
      all_venue_shows = Show.query.filter(Show.venue_id == v.id)
      for show in all_venue_shows:
        show_dic = {}
        show_dic['artist_id'] = show.artist_id
        required_fields =  Artist.query.with_entities(Artist.name, Artist.image_link).filter(Artist.id == show.artist_id).first()
        show_dic['artist_name'] = required_fields[0]
        show_dic['artist_image_link'] = required_fields[1]
        show_dic['start_time'] = str(show.date)
        if(show.date > current_date):
          upcoming_shows.append(show_dic)
        else:
          past_shows.append(show_dic)
      data['past_shows'] = past_shows
      data['upcoming_shows'] = upcoming_shows
      data['upcoming_shows_count'] = len(upcoming_shows)
      data['past_shows_count'] = len(past_shows)
  # print(data)
  print(data)
  return render_template('pages/show_venue.html', venue=data)

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

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists') #Done 
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.with_entities(Artist.id , Artist.name) 
  print(data)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term')
  result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []
  for artist in result:
    dic = {
      'id': artist.id,
      'name':artist.name, 
      'num_upcoming_shows':Show.query.filter(Artist.id == artist.id).count()
    }
    data.append(dic)

  response = {
    "count" : len(result),
    "data" : data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = {} 
  artist = Artist.query.filter(Artist.id == artist_id).first()
  if(artist == None):
    return render_template('errors/404.html') 
  
  data = {} 
  data['id'] = artist.id
  data['name'] = artist.name
  if(artist.genres == None):
    data['genres'] = "" 
  else:
    data['genres'] = artist.genres

  data['city'] = artist.city
  data['state'] = artist.state
  data['phone'] = artist.phone
  data['website'] = artist.website
  data['facebook_link'] = artist.facebook_link
  data['seeking_venue'] = artist.seeking_venue
  data['seeking_description'] = artist.seeking_venue_description
  data['image_link'] = artist.image_link
  past_shows = [] 
  upcoming_shows = []
  current_date = datetime.now()
  all_venue_shows = Show.query.filter(Show.artist_id == artist.id)
  for show in all_venue_shows:
    show_dic = {}
    show_dic['venue_id'] = show.venue_id
    required_fields =  Venue.query.with_entities(Venue.name, Venue.image_link).filter(Venue.id == show.venue_id).first()
    show_dic['venue_name'] = required_fields[0]
    show_dic['venue_image_link'] = required_fields[1]
    show_dic['start_time'] = str(show.date)
    if(show.date > current_date):
      upcoming_shows.append(show_dic)
    else:
      past_shows.append(show_dic)
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['upcoming_shows_count'] = len(upcoming_shows)
  data['past_shows_count'] = len(past_shows)


  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
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
  venue={
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

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():  
  data = [] 
  shows = Show.query.all()
  path =  'pages/shows.html'
  try:
    for show in shows : 
      dic = {} 
      dic['venue_id'] = show.venue_id 
      dic['aritst_id'] = show.artist_id
      dic['start_time'] = str(show.date)
      venue_name = Venue.query.filter(Venue.id == show.venue_id).first().name
      dic['venue_name'] = venue_name
      artist_required_field = Artist.query.with_entities(Artist.name , Artist.image_link).filter(Artist.id == show.artist_id).first()
      dic['artist_name'] = artist_required_field[0] 
      dic['artist_image_link'] = artist_required_field[1]
      data.append(dic)
  except:
    path = 'errors/500.html'
  finally:
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

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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

if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run()



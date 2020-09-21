from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL,ValidationError , Length
from wtforms_validators import Alpha


state_choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
genres_choices = [
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]

def validate_name():
   # message = 'Must be between %d and %d characters long.' % (min, max)
    message = 'Invalid Name (maybe you included numbers ) '

    def _validate_name(form, field):
        s = field.data
        if not all(x.isalpha() or x.isspace() for x in s):
            raise ValidationError(message)

    return _validate_name

def validate_phone():
   # message = 'Must be between %d and %d characters long.' % (min, max)
    message = 'Invalid Number (maybe you included characters in it or a \'+\' sign ) '

    def _validate_phone(form, field):
        s = field.data
        if not s.isnumeric():
            raise ValidationError(message)

    return _validate_phone

def validate_city():
   # message = 'Must be between %d and %d characters long.' % (min, max)
    message = 'Invalid City (maybe you included numbers ) '

    def _validate_city(form, field):
        s = field.data
        if not all(x.isalpha() or x.isspace() for x in s):
            raise ValidationError(message)

    return _validate_city


class ShowForm(Form):
    artist_id = StringField(
        'artist_id', validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired() , validate_city()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices= state_choices
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired() , validate_phone()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=genres_choices
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired() , validate_name()]
    )
    city = StringField(
        'city', validators=[DataRequired() , validate_city()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],choices = state_choices       
    )
    phone = StringField(
        'phone',[ DataRequired() , validate_phone()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=genres_choices
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
   
       


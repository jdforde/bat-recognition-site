from curses import meta
import enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# 0 = clear, 1 = one third, 2 = two thirds, 3 = overcast
class CloudCover(enum.Enum):
    clear = 0
    one_third = 1
    two_thirds = 2
    overcast = 3

# 0 = past 24 hours, 1 = start of recording, 2 = end of recording
class TimeOfDay(enum.Enum):
    pastDay = 0
    startOfRecording = 1
    endOfRecording = 2

# 0 = none, 1 = fog, 2 = light rain, 3 = hard rain, 4 = hail, 5 = snow
class Precipitation(enum.Enum):
    noPrecipitation = 0
    fog = 1
    lightRain = 2
    hardRain = 3
    hail = 4
    snow = 5
    
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metadata_id = db.Column(db.Integer, db.ForeignKey('meta.id'), nullable=False)
    meta = db.relationship('Metadata', backref=db.backref('sumbmissions', lazy=True))
    angle1_part1 = db.Column(db.Integer, db.ForeignKey('video1.id'), nullable=False)
    video1 = db.relationship('Video', backref=db.backref('sumbmissions', lazy=True))
    angle1_part2 = db.Column(db.Integer, db.ForeignKey('video2.id'), nullable=False)
    video2 = db.relationship('Video', backref=db.backref('sumbmissions', lazy=True))
    angle2_part1 = db.Column(db.Integer, db.ForeignKey('video3.id'), nullable=False)
    video3 = db.relationship('Video', backref=db.backref('sumbmissions', lazy=True))
    angle2_part2 = db.Column(db.Integer, db.ForeignKey('video4.id'), nullable=False)
    video4 = db.relationship('Video', backref=db.backref('sumbmissions', lazy=True))

    def __repr__(self):
        return '<Submission %r>' % self.id

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(80), unique=True, nullable=False)
    link = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Video %r>' % self.id

class Bat_Sighting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    video = db.relationship('Video', backref=db.backref('bat_sightings', lazy=True))
    minutes_passed = db.Column(db.Double, unique=False, nullable=False)
    bat_count = db.Column(db.Booolean, unique=False, nullable=False)

    def __repr__(self):
        return '<Bat_Sighting %r>' % self.id

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_recorded = db.Column(db.Date, unique=True, nullable=False)
    sunset_time = db.Column(db.Time, unique=True, nullable=False)
    new_moon = db.Column(db.Date, unique=True, nullable=False)
    team_expert = db.Column(db.Integer, db.ForeignKey('person1.id'), nullable=False)
    person1 = db.relationship('Person', backref=db.backref('metadata', lazy=True))
    recorder = db.Column(db.Integer, db.ForeignKey('person2.id'), nullable=False)
    person2 = db.relationship('Person', backref=db.backref('metadata', lazy=True))
    participant = db.Column(db.Integer, db.ForeignKey('person1.id'), nullable=False)
    person1 = db.relationship('Person', backref=db.backref('metadata', lazy=True))

    def __repr__(self):
        return '<Metadata %r>' % self.id

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.id

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metadata_id = db.Column(db.Integer, db.ForeignKey('meta.id'), nullable=False)
    meta = db.relationship('Metadata', backref=db.backref('weather', lazy=True))
    is_sunset = db.Column(db.Booolean, unique=False, nullable=False)
    temp = db.Column(db.Double, unique=True, nullable=False)
    relative_humidity = db.Column(db.Double, unique=True, nullable=False)
    wind = db.Column(db.Double, unique=True, nullable=False)
    cloud_cover = db.Column(CloudCover, unique=False, nullable=False)

    def __repr__(self):
        return '<Weather %r>' % self.id

class Precipitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metadata_id = db.Column(db.Integer,db.ForeignKey('meta.id'), nullable=False)
    meta = db.relationship('Metadata', backref=db.backref('precipitation', lazy=True))
    time_of_day = db.Column(TimeOfDay, unique=False, nullable=False)
    precipitation_type = db.Column(Precipitation, unique=False, nullable=False)

    def __repr__(self):
        return '<Precipitation %r>' % self.id
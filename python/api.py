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
    metadata_id = db.Column(db.Integer, unique=False, nullable=False)
    angle1_part1 = db.Column(db.Integer, unique=False, nullable=False)
    angle1_part2 = db.Column(db.Integer, unique=False, nullable=False)
    angle2_part1 = db.Column(db.Integer, unique=False, nullable=False)
    angle2_part2 = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<EmergenceCountSurvey %r>' % self.expert

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(80), unique=True, nullable=False)
    link = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Video %r>' % self.id

class Bat_Sighting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, unique=True, nullable=False)
    minutes_passed = db.Column(db.Double, unique=False, nullable=False)
    bat_count = db.Column(db.Booolean, unique=False, nullable=False)

    def __repr__(self):
        return '<BatData %r>' % self.bat_count

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_recorded = db.Column(db.Date, unique=True, nullable=False)
    sunset_time = db.Column(db.Time, unique=True, nullable=False)
    new_moon = db.Column(db.Date, unique=True, nullable=False)
    team_expert = db.Column(db.Integer, unique=True, nullable=False)
    recorder = db.Column(db.Integer, unique=True, nullable=False)
    participant = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return '<BatData %r>' % self.bat_count

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return '<BatData %r>' % self.bat_count

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metadata_id = db.Column(db.Integer, unique=False, nullable=False)
    is_sunset = db.Column(db.Booolean, unique=False, nullable=False)
    temp = db.Column(db.Double, unique=True, nullable=False)
    relative_humidity = db.Column(db.Double, unique=True, nullable=False)
    wind = db.Column(db.Double, unique=True, nullable=False)
    cloud_cover = db.Column(CloudCover, unique=False, nullable=False)

    def __repr__(self):
        return '<BatData %r>' % self.bat_count

class Precipitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metadata_id = db.Column(db.Integer, unique=False, nullable=False)
    time_of_day = db.Column(TimeOfDay, unique=False, nullable=False)
    precipitation_type = db.Column(Precipitation, unique=False, nullable=False)

    def __repr__(self):
        return '<EmergenceCountSurvey %r>' % self.expert
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Song(db.Model):
    __tablename__="song"
    id = db.Column(db.Integer(), primary_key=True)
    song_title= db.Column(db.String(100), nullable=False)
    song_duration= db.Column(db.Integer(), nullable=False)
    song_upload_date =db.Column(db.DateTime(), default=db.func.now(), nullable=False)

class Podcast(db.Model):
    __tablename__="podcast"
    id = db.Column(db.Integer(), primary_key=True)
    podcast_title = db.Column(db.String(100), nullable=False)
    podcast_duration= db.Column(db.Integer(), nullable=False)
    podcast_upload_time= db.Column(db.DateTime(), default=db.func.now(), nullable=False)
    podcast_host = db.Column(db.String(100), nullable=False)
    podcast_participants= db.Column(db.String(100), nullable=True)

    @property
    def participants(self):
        return [x for x in self.podcast_participants.split(",")]
    @participants.setter
    def participants (self, value):
        self.podcast_participants += ',%s' % value

class AudioBook(db.Model):
    __tablename__="audiobook"
    id = db.Column(db.Integer(), primary_key=True)
    audiobook_title = db.Column(db.String(100), nullable=False)
    book_author = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100), nullable=False)
    audiobook_duration= db.Column(db.Integer(), nullable=False)
    audiobook_upload_date= db.Column(db.DateTime(), default=db.func.now(), nullable=False)

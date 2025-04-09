from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# A table of users in database
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    # information
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    register_time = db.Column(db.DateTime, default=datetime.now)
    gender = db.Column(db.String(10), nullable=True)
    icon = db.Column(db.String(128), default='../static/avatars/default.jpg')
    introduction = db.Column(db.String(64), nullable=True)
    authority = db.Column(db.Integer, default=0, nullable=False)
    ban = db.Column(db.Boolean, default=False, nullable=False)
    comedy = db.Column(db.Boolean, default=False, nullable=False)
    action = db.Column(db.Boolean, default=False, nullable=False)
    love = db.Column(db.Boolean, default=False, nullable=False)
    cartoon = db.Column(db.Boolean, default=False, nullable=False)
    science = db.Column(db.Boolean, default=False, nullable=False)
    suspense = db.Column(db.Boolean, default=False, nullable=False)
    war = db.Column(db.Boolean, default=False, nullable=False)
    thriller = db.Column(db.Boolean, default=False, nullable=False)

    # encrypt password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # translate password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# A table of friends between two user
class Friends(db.Model):
    __tablename__ = "friends"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    relationship = db.Column(db.String(10), default='friend')


# A table of friends between two user
class Friend_Application(db.Model):
    __tablename__ = "friend_application"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'))
    reason = db.Column(db.String(200), nullable=True)


# A table of comments of movies
class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    title = db.Column(db.String(32), nullable=False)
    text = db.Column(db.String(128), nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)
    like_num = db.Column(db.Integer, default=0)
    grade = db.Column(db.Integer, default=0)


# A table of likes of comments
class Comment_Like(db.Model):
    __tablename__ = "comment_like"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # movie = db.relationship('movie', backref=db.backref('Movie', lazy='dynamic'))


# A table of movies
class Movie(db.Model):
    __tablename__ = "movie"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(32), nullable=False)
    release_time = db.Column(db.Date, nullable=True)
    pic_path = db.Column(db.String(64), nullable=True)
    introduction = db.Column(db.String(64), nullable=True)
    popular = db.Column(db.String(64), nullable=False)
    vote_average = db.Column(db.Integer, default=0)
    vote_count = db.Column(db.Integer, default=0)
    is_delete = db.Column(db.Boolean, default=False, nullable=False)
    comedy = db.Column(db.Boolean, default=False, nullable=False)
    action = db.Column(db.Boolean, default=False, nullable=False)
    love = db.Column(db.Boolean, default=False, nullable=False)
    cartoon = db.Column(db.Boolean, default=False, nullable=False)
    science = db.Column(db.Boolean, default=False, nullable=False)
    suspense = db.Column(db.Boolean, default=False, nullable=False)
    war = db.Column(db.Boolean, default=False, nullable=False)
    thriller = db.Column(db.Boolean, default=False, nullable=False)


# A table of movie stage photo
class Movie_stage(db.Model):
    __tablename__ = "movie_stage"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    pic_path = db.Column(db.String(64), nullable=False)


# movie feedback
class Advise(db.Model):
    __tablename__ = "advise"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(32), nullable=False)
    text = db.Column(db.String(128), nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)


# A table of likes of movie
class Movie_Like(db.Model):
    __tablename__ = "movie_like"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    # movie = db.relationship('movie', backref=db.backref('Movie', lazy='dynamic'))


# A table of collect of movie
class Movie_Collect(db.Model):
    __tablename__ = "movie_collect"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    # movie = db.relationship('movie', backref=db.backref('Movie', lazy='dynamic'))


# A table of the grades of movie
class Movie_Grade(db.Model):
    __tablename__ = "movie_grade"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    grade = db.Column(db.Integer, nullable=True)
    # movie = db.relationship('movie', backref=db.backref('Movie', lazy='dynamic'))


# A table of message list
class Mess(db.Model):
    __tablename__ = "message"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    room = db.Column(db.String(64), nullable=False)
    read = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# A table of chatroom
class Room(db.Model):
    __tablename__ = "room"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room = db.Column(db.String(64), nullable=False)
    change_time = db.Column(db.DateTime, default=datetime.now, index=True)
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    unread = db.Column(db.Integer, default=0)


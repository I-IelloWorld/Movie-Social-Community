import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'panacea_g3'

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'panacea.db')

	SQLALCHEMY_TRACK_MODIFICATIONS = True

	AVATARS_SAVE_PATH = os.path.join(basedir, 'static/temporary')
	ICON_SAVE_PATH = os.path.join(basedir, 'static/avatars')
	MOVIE_SAVE_PATH = os.path.join(basedir, 'static/stage photo')
	AVATARS_SERVE_LOCAL = True
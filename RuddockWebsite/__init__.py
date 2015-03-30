from datetime import datetime
from flask import Flask, g
from sqlalchemy import create_engine

from RuddockWebsite import config, constants
from RuddockWebsite.modules import account, admin, auth, hassle, users

app = Flask(__name__)
app.debug = False
app.secret_key = config.SECRET_KEY

# Maximum file upload size, in bytes.
app.config['MAX_CONTENT_LENGTH'] = constants.MAX_CONTENT_LENGTH

# Update jinja global functions
app.jinja_env.globals.update(current_year=lambda: datetime.now().year)

# Load blueprint modules
app.register_blueprint(account.blueprint, url_prefix='/account')
app.register_blueprint(admin.blueprint, url_prefix='/admin')
# Auth blueprint has no prefix, since not all endpoints have the same prefix.
app.register_blueprint(auth.blueprint)
app.register_blueprint(hassle.blueprint, url_prefix='/hassle')
app.register_blueprint(users.blueprint, url_prefix='/users')

# Create database engine object.
engine = create_engine(config.DB_URI, convert_unicode=True)

@app.before_request
def before_request():
  ''' Logic executed before request is processed. '''

  # Connect to the database and publish it in flask.g
  g.db = engine.connect()

@app.teardown_request
def teardown_request(exception):
  ''' Logic executed after every request is finished. '''

  # Close database connection.
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

# After initialization, import the routes.
from RuddockWebsite import routes
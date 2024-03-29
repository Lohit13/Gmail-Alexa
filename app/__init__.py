from flask import Flask

app = Flask(__name__)

app.config.from_object('config')

from app.controllers import gmail

app.register_blueprint(gmail)


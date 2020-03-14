from flask import Flask
from flask.logging import create_logger

app = Flask(__name__)
logger = create_logger(app)

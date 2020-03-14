# add gunicorn logger
import logging
from app import app
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
# --level error is default
app.logger.setLevel(gunicorn_logger.level) # pylint: disable=no-member


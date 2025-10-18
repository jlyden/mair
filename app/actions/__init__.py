from flask import Blueprint

bp = Blueprint('actions', __name__)

from app.actions import routes
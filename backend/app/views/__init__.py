from flask import Blueprint

blueprint = Blueprint('views', __name__)

from app.views import user
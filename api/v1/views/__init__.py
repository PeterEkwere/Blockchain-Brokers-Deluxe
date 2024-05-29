#!/usr/bin/python3
"""
    Blueprint for API
    Author: Peter Ekwere
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
#from api.v1.views.recipe_ingredients import *
#from api.v1.views.recipe import *
#from api.v1.views.ingredients import *
from api.v1.views.users import *
from api.v1.views.services import *
# from api.v1.views.login import *
#!/usr/bin/python3
"""
    This Module contains the status Route
    Author: Peter Ekwere
"""
from models.user import User
#from models import storage
from api.v1.views import app_views
from flask import jsonify, render_template
from api.v1.extensions import cache
from flask import session


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime 
import requests
import os

user_bp = Blueprint("user",__name__,url_prefix = "/users")

# create a user
@user_bp.route("",methods = ["POST"])
def create_user():
    response_body = request.get_json()
    if "name" not in response_body or "tennis_level" not in response_body:
        return jsonify({"details":" Invalid data"}), 400
    
    new_user = User.from_dict(response_body)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"user":
                   {"id":new_user.user_id,
                    "name":new_user.name,
                    "tennis_level":new_user.tennis_level,
                    "zip_code":new_user.zip_code
                    }}), 201
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
# get a user info
@user_bp.route("/<user_id>", methods = ["GET"])
def get_one_user(user_id):
    users = validate_user(User,user_id)
    if 


# update user 
@user_bp.route("/<user_id", methods = ["PUT"])
def update_user(user_id):
    users = validate_user(User,user_id)
    request_data = request.get_json()

    users.name = request_data["name"]
    users.tennis_level = request_data["tennis_level"]
    users.zip_code = request_data["zip_code"]

    db.seesion.commit()

    return jsonify({"user":{
                    "id":new_user.user_id,
                    "name":new_user.name,
                    "tennis_level":new_user.tennis_level,
                    "zip_code":new_user.zip_code
    }}), 200

# delete user
@user_bp.route("/<user_id>", methods = ["DELETE"])
def delete_user(user_id):
    users = validate_user(User, user_id)

    db.seesion.delete(users)
    db.session.commit()

    return {"details": f'User {user_id} deleted successfully!'}


# helper funtion (validate_user)
def validate_user(model, user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        abort(make_response({"mes":"id is invalide input"}, 400))
    
    user = model.query.get(user_id)
    if user is None:
        abort(make_response({"msg": "User not found"}, 404))
    return user 
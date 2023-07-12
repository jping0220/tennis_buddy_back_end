from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.user import User
# from datetime import datetime 
import requests
import os


user_bp = Blueprint("user",__name__, url_prefix = "/users")
def getCurrentUserId():
    return "laura1234"
    # once JWT Bearer authentication is hooked up
    #return request_security_token.sub

# create a user
@user_bp.route("", methods=["POST"])

def create_user():
    ''''User is able to list their information on the site'''
    request_body = request.get_json()
    new_user = User.from_dict(request_body)
    #new_user.user_id = getCurrentUserId()

    # if "name" not in response_body or "tennis_level" not in response_body:
    #     return jsonify({"details":" Invalid data"}), 400

    db.session.add(new_user)
    db.session.commit()

    return {"user":new_user.to_dict()}, 201


# get all users 
# @user_bp.route("",methods=["GET"])
# def get_all_users():
#     response = []
#     all_users = User.query.all()

#     for user in all_users:
#         response.append(user.to_dict())

#     return jsonify(response),200


# get one user info
@user_bp.route("<user_id>", methods = ["GET"])
def get_one_user(user_id):
    ''''User is able to see their information on the site'''
    user = validate_user(User,user_id)
    return {"user":user.to_dict()}, 200


# update user 
@user_bp.route("/<user_id>", methods = ["PATCH"])
def update_user(user_id):
    user = validate_user(User,user_id)
    request_data = request.get_json()
    
    if request_data.get("preferences"):
        user.preferences = request_data["preferences"]
    elif request_data.get("name"):
        user.name = request_data["name"]
    elif request_data.get("tennis_level"):
        user.tennis_level = request_data["tennis_level"]
    elif request_data.get("zip_code"):
        user.zip_code = request_data["zip_code"]
    elif request_data.get("email"):
        user.email = request_data["email"]
    

    db.session.commit()

    return {"user":user.to_dict()}, 200


# delete user
@user_bp.route("/<user_id>", methods = ["DELETE"])
def delete_user(user_id):
    user = validate_user(User, user_id)

    db.session.delete(user)
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

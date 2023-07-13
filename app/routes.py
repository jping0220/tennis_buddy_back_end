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

    # print(new_user.tennis_level)

    db.session.add(new_user)
    db.session.commit()

    # print({"user":new_user.to_dict()})

    return {"user":new_user.to_dict()}, 201


# get all users 
@user_bp.route("",methods=["GET"])
def get_all_users():
    response = []
    all_users = User.query.all()

    for user in all_users:
        response.append(user.to_dict())

    return jsonify(response),200


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
    

    # update_user = request_data
    if request_data.get("preferences"):
        user.preferences = request_data["preferences"]
    if request_data.get("name"):
        user.name = request_data["name"]
    if request_data.get("tennis_level"):
        user.tennis_level = request_data["tennis_level"]
    if request_data.get("zip_code"):
        user.zip_code = request_data["zip_code"]
    if request_data.get("email"):
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
        abort(make_response({"msg":"id is invalide input"}, 400))
    
    user = model.query.get(user_id)
    if user is None:
        abort(make_response({"msg": "User not found"}, 404))
    return user 



# new BluePrint here for public
# GET all users info 
# GET user info by multiple filters 
# 

public_bp = Blueprint("",__name__, url_prefix = "/")

@public_bp.route("", methods=["GET"])
def get_all_users():
    response = []
    all_users = User.query.all()

    for user in all_users:
        response.append(user.to_dict())

    return jsonify(response),200



# http://127.0.0.1:5000/search?zip_code=98022      try this in postman with your database
# http://127.0.0.1:5000/search?tennis_level=4.0    try this in postman with your database
@public_bp.route("/search", methods=["GET"])
def search_by_zip_code_and_tennis_level():

    zip_code = request.args.get("zip_code")
    tennis_level = request.args.get("tennis_level")
    # print(tennis_level)
   
    response = []

    # user_by_zipcode = User.query.filter_by(zip_code=zip_code).all()
    # if not user_by_zipcode:
    #     abort(make_response(
    #         {"message": f"{zip_code} not found in {zip_code}"}, 404))
    # for user in user_by_zipcode :
    #     response.append(user.to_dict())


    if zip_code:
        users = User.query.filter_by(zip_code=zip_code).all()
        if not users:
            abort(make_response({"message": f"No users found with zip code {zip_code}"}, 404))
        for user in users:
            response.append(user.to_dict())

    if tennis_level:
        tennis_level = float(tennis_level)
        users = User.query.filter_by(tennis_level=tennis_level).all()
        if not users:
            abort(make_response({"message": f"No users found with tennis level {tennis_level}"}, 404))
        for user in users:
            response.append(user.to_dict())

    if not response:
        abort(make_response({"message": "No users found"}, 404))


    return jsonify(response), 200




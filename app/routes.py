from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.user import TennisUser
from dotenv import load_dotenv
# from datetime import datetime 
import requests
import os

load_dotenv()

user_bp = Blueprint("tennis_user",__name__, url_prefix = "/users")
def getCurrentUserId():
    return "laura1234"
    # once JWT Bearer authentication is hooked up
    #return request_security_token.sub


# create a user
@user_bp.route("", methods=["POST"])
def create_user():
    ''''User is able to list their information on the site'''
    request_body = request.get_json()
    new_user = TennisUser.from_dict(request_body)
    #new_user.user_id = getCurrentUserId()

    print(new_user.tennis_level)

    db.session.add(new_user)
    db.session.commit()

    # print({"user":new_user.to_dict()})

    return {"user":new_user.to_dict()}, 201


# get all users 
@user_bp.route("",methods=["GET"])
def get_all_users():
    response = []
    all_users = TennisUser.query.all()

    for user in all_users:
        response.append(user.to_dict())

    return jsonify(response),200


# get one user info
@user_bp.route("<user_id>", methods = ["GET"])
def get_one_user(user_id):
    ''''User is able to see their information on the site'''
    user = validate_user(TennisUser,user_id)
    return {"user":user.to_dict()}, 200


# update user 
@user_bp.route("/<user_id>", methods = ["PATCH"])
def update_user(user_id):
    user = validate_user(TennisUser,user_id)
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
    user = validate_user(TennisUser, user_id)

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


def validate_numeric_input(input):
    input = float(input)
    if input:
        return True
    else:
        abort(make_response(
            {"message": f"{input} invalid"}, 400))


path = "https://api.zip-codes.com/ZipCodesAPI.svc/1.0/FindZipCodesInRadius"

ZIP_CODES_KEY = os.environ.get("ZIP_CODES_KEY")

def create_params(zip_code):
    query_params = {
        "zipcode": zip_code,
        "minimumradius": 0,
        "maximumradius": 20,
        "country": "ALL",
        "key": ZIP_CODES_KEY
    }
    return query_params


def construct_request_for_zip_code(query_params):
    response = requests.get(path, params=query_params)
    response_body = response.json()
    return response_body


def get_list_of_zip_codes(zip_code):
    query_params = create_params(zip_code)
    response_body = construct_request_for_zip_code(query_params)
    closest_zip_codes = []
    list_of_cities = response_body['DataList']
    for item in list_of_cities:
        closest_zip_codes.append(item["Code"])
    return closest_zip_codes



@public_bp.route("", methods=["GET"])
def search_by_zip_code_and_tennis_level():
    response = []
    session = db.session
    tennis_level = None

    #calling the API to populate the closest_zip_codes list:
    closest_zip_codes = None

    #taking args from request:
    args = request.args
    if not args:
            abort(make_response(
                {"message": f"invalid params"}, 400))
    
    for k, v in args.items():
        if k == "zip_code":
            if validate_numeric_input(v):
                closest_zip_codes = get_list_of_zip_codes(v)
        elif k == "tennis_level":
            if validate_numeric_input(v):
                tennis_level = v
    #query:
    if tennis_level != None and len(closest_zip_codes) > 0:
                result = session.query(TennisUser).filter(TennisUser.zip_code.in_(
                closest_zip_codes)).filter(TennisUser.tennis_level == tennis_level)

    elif tennis_level != None and closest_zip_codes == None:
        result = session.query(TennisUser).filter(TennisUser.tennis_level == tennis_level)
    
    elif tennis_level == None and len(closest_zip_codes) > 0:
        result = session.query(TennisUser).filter(TennisUser.zip_code.in_(
        closest_zip_codes))
    

    for row in result:
        response.append(row.to_dict())

    return jsonify(response), 200


    # if not args:
    #     abort(make_response(
    #                 {"message": f"invalid params"}, 400))
    # argsdict = {}
    # for k, v in args.items():
    #     if validate_numeric_input(v):
    #         argsdict[k] = v
    # query = TennisUser.query.filter_by(**argsdict)

    # for user in query:
    #     response.append(user.to_dict())
    # return jsonify(response), 200


#-----query for list of zip codes:
#tennis_level = 2
#closest_zip_codes = [98029,98020]
# response = []
# result = session.query(TennisUser).filter(TennisUser.zip_code.in_(closest_zip_codes),TennisUser.tennis_level.like(tennis_level) )
# for row in result:
#     response.append(row)


###-------------code for the zip API:

# session = db.session
#    closest_zip_codes = [98008, 98074]
#     tennis_level = 3

#     #calling the API to populate the closest_zip_codes list:

#     response = []

#     result = session.query(TennisUser).filter(TennisUser.zip_code.in_(
#         closest_zip_codes)).filter(TennisUser.tennis_level == tennis_level)

#     for row in result:
#         response.append(row.to_dict())

#     return jsonify(response), 200


##____________________code that works without API:
# response = []
#   args = request.args
#    if not args:
#           abort(make_response(
#                {"message": f"invalid params"}, 400))
#     argsdict = {}
#     for k, v in args.items():
#         if validate_numeric_input(v):
#             argsdict[k] = v
#     query = TennisUser.query.filter_by(**argsdict)

#     for user in query:
#         response.append(user.to_dict())
#     return jsonify(response), 200

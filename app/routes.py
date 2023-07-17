from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.user import TennisUser
from dotenv import load_dotenv
# from datetime import datetime 
import requests
import os

load_dotenv()


#-----------------------PROTECTED ROUTES ---------------------------


user_bp = Blueprint("tennis_user",__name__, url_prefix = "/users")


#new route with auth 0
# create a user
#add this @require_auth(None)
@user_bp.route("", methods=["POST"])
def create_user():
    ''''User is able to list their information on the site'''

    request_body = request.get_json()
    new_user = TennisUser.from_dict(request_body)
    new_user.token = current_token.sub


    db.session.add(new_user)
    db.session.commit()

    return {"user": new_user.to_dict()}, 201


#_____________________________________
# create new user route (old route intact)
@user_bp.route("", methods=["POST"])
def create_user():
    ''''User is able to list their information on the site'''

    # Código orginal sin tocar:
    request_body = request.get_json()
    new_user = TennisUser.from_dict(request_body)
    #new_user.user_id = getCurrentUserId()

    print(new_user.tennis_level)

    db.session.add(new_user)
    db.session.commit()

    # print({"user":new_user.to_dict()})

    return {"user":new_user.to_dict()}, 201


# get all users - we won't use this route:
# @user_bp.route("",methods=["GET"])
# def get_all_users():
#     response = []
#     all_users = TennisUser.query.all()

#     for user in all_users:
#         response.append(user.to_dict())

#     return jsonify(response),200


#New route with auth:
#get user info
#add decorator: @require_auth(None)
@user_bp.route("", methods=["GET"])
def get_one_user():
    ''''User is able to see their information on the site'''
    result = session.query(TennisUser).filter(
        TennisUser.token == current_token.sub)
    if result is None:
        abort(make_response({"msg": "User not found"}, 404))
    
    return {"user": result.to_dict()}, 200


#__________________________________
# get one user info (old route leave intact)
@user_bp.route("<user_id>", methods = ["GET"])
def get_one_user(user_id):
    ''''User is able to see their information on the site'''
    user = validate_user(TennisUser,user_id)
    return {"user":user.to_dict()}, 200
#________________________________________



#new route with auth:
#update user info:
#add decorator: @require_auth(None)
@user_bp.route("", methods=["PATCH"])
def update_user(user_id):
    ''''User is able to modify their information on the site'''
    #get the user:
    result = session.query(TennisUser).filter(
        TennisUser.token == current_token.sub)
    if result is None:
        abort(make_response({"msg": "User not found"}, 404))
    
    #get new info:
    request_data = request.get_json()

    # update_user = request_data
    if request_data.get("preferences"):
        result.preferences = request_data["preferences"]
    if request_data.get("name"):
        result.name = request_data["name"]
    if request_data.get("tennis_level"):
        result.tennis_level = request_data["tennis_level"]
    if request_data.get("zip_code"):
        result.zip_code = request_data["zip_code"]
    if request_data.get("email"):
        result.email = request_data["email"]

    db.session.commit()

    return {"user": result.to_dict()}, 200

#___________________________________
# update user (old route intact)
@user_bp.route("/<user_id>", methods = ["PATCH"])
def update_user(user_id):
    ''''User is able to modify their information on the site'''
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
#_____________________________________________



#new route
#add decorator: @require_auth(None)
@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    '''User can delete their profile'''
    result = session.query(TennisUser).filter(
        TennisUser.token == current_token.sub)
    if result is None:
        abort(make_response({"msg": "User not found"}, 404))

    db.session.delete(result)
    db.session.commit()

    return {"details": f'User {user_id} deleted successfully!'}


#___________________________________________
# delete user (old route intact)
@user_bp.route("/<user_id>", methods = ["DELETE"])
def delete_user(user_id):
    '''User can delete their profile'''
    user = validate_user(TennisUser, user_id)

    db.session.delete(user)
    db.session.commit()

    return {"details": f'User {user_id} deleted successfully!'}
#_____________________________________________________

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


    



# -------------------PUBLIC ROUTE-------------------------------------

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
    closest_zip_codes = []
    result = []
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

    elif tennis_level != None and not closest_zip_codes:
        result = session.query(TennisUser).filter(TennisUser.tennis_level == tennis_level)
    
    elif tennis_level == None and len(closest_zip_codes) > 0:
        result = session.query(TennisUser).filter(TennisUser.zip_code.in_(
        closest_zip_codes))
    
    
    for row in result:
        response.append(row.to_dict())

    return jsonify(response), 200


#-----query for list of zip codes:
#tennis_level = 2
#closest_zip_codes = [98029,98020]
# response = []
# result = session.query(TennisUser).filter(TennisUser.zip_code.in_(closest_zip_codes),TennisUser.tennis_level.like(tennis_level) )
# for row in result:
#     response.append(row)

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

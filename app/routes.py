from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.user import TennisUser
from dotenv import load_dotenv
from authlib.integrations.flask_oauth2 import ResourceProtector, current_token
from .validator import Auth0JWTBearerTokenValidator
import requests
import os

load_dotenv()

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "dev-6y0ycamcr4u3vu7z.us.auth0.com",
    "https://tennis_buddy"
)
require_auth.register_token_validator(validator)




#-----------------------PROTECTED ROUTES WITH AUTHENTICATION ---------------------------

#For auth0 change this route to "users/me"
user_bp = Blueprint("tennis_user", __name__, url_prefix="/users/me")



def get_authenticated_user_id():
    return current_token.sub


# create a user
@user_bp.route("", methods=["POST"])
@require_auth(None)
def create_user():
    ''''User is able to list their information on the site'''
    #Checking if user already has a profile:
    session = db.session
    auth_user_id = get_authenticated_user_id()
    result = session.query(TennisUser).filter(
        TennisUser.auth_user_id == auth_user_id).first()
    if not result:
        request_body = request.get_json()
        print(request_body)
        new_user = TennisUser.from_dict(request_body)
        new_user.auth_user_id = get_authenticated_user_id()
        print(new_user.auth_user_id)

        db.session.add(new_user)
        db.session.commit()

        return {"user": new_user.to_dict()}, 201
    
    abort(make_response({"msg": "User profile already exists"}, 409))

#get user info
@user_bp.route("", methods=["GET"])
@require_auth(None)
def get_one_user():
    ''''User is able to see their information on the site'''
    session = db.session
    auth_user_id = get_authenticated_user_id()
    
    result = session.query(TennisUser).filter(
        TennisUser.auth_user_id == auth_user_id).first()
    
    if not result:
        abort(make_response({"msg": "User not found"}, 404))

    return {"user": result.to_dict()}, 200

#update user info:
@user_bp.route("", methods=["PATCH"])
@require_auth(None)
def update_user():
    ''''User is able to modify their information on the site'''
    session = db.session
    auth_user_id = get_authenticated_user_id()
    #get the user:
    existing_user = session.query(TennisUser).filter(
        TennisUser.auth_user_id == auth_user_id).first()
    
    if existing_user is None:
        abort(make_response({"msg": "User not found"}, 404))

    #get new info:
    request_data = request.get_json()
    print(request_data['name'])

    
    if request_data.get("preferences"):
        existing_user.preferences = request_data["preferences"]
    if request_data.get("name"):
        existing_user.name = request_data["name"]
    if request_data.get("tennis_level"):
        existing_user.tennis_level = request_data["tennis_level"]
    if request_data.get("zip_code"):
        existing_user.zip_code = request_data["zip_code"]
    if request_data.get("email"):
        existing_user.email = request_data["email"]

    print(f"second {existing_user.name}")
    db.session.commit()

    return {"user": existing_user.to_dict()}, 200

#delete user
@user_bp.route("", methods=["DELETE"])
@require_auth(None)
def delete_user():
    '''User can delete their profile'''
    session = db.session
    auth_user_id = get_authenticated_user_id()
    print(auth_user_id)
    result = session.query(TennisUser).filter(
        TennisUser.auth_user_id == auth_user_id).first()
    if result is None:
        abort(make_response({"msg": "User not found"}, 404))

    db.session.delete(result)
    db.session.commit()

    return {"details": f'User {auth_user_id} deleted successfully!'}

# -------------------PUBLIC ROUTE-------------------------------------


public_bp = Blueprint("", __name__, url_prefix="/search")


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
        result = session.query(TennisUser).filter(
            TennisUser.tennis_level == tennis_level)

    elif tennis_level == None and len(closest_zip_codes) > 0:
        result = session.query(TennisUser).filter(TennisUser.zip_code.in_(
            closest_zip_codes))

    for row in result:
        response.append(row.to_dict())

    return jsonify(response), 200


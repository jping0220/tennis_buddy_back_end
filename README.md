# tennis_buddy_back_end

## Overview and Purpose
The Tennis Buddy API provides endpoints to handle user registration, profile management and search functions.


## Getting Started:
Clone this repository:
```
git clone https://github.com/jping0220/tennis_buddy_back_end
```
Activate virtual env:
```
$ source env/bin/activate
```
Install dependencies:
```
pip3 install -r requirements.txt
```
## API Documentation
Authenticated routes:
* POST /users/me
* Description: Register a new user.
* Authentication: Bearer token (JWT) required in the Authorization header.
* Request Body:
```
{
  "name": "John Doe",
  "email": "john@example.com",
  "zip_code": 98029,
  "tennis_level": 4.5,
  "preferences" : "Play during the morning"
}
```
* Response:
json
```
  {
  "user": 
  {"name": "John Doe",
  "email": "john@example.com",
  "zip_code": 98029,
  "tennis_level": 4.5,
  "preferences" : "Play during the morning"}
  }
```

* GET /users/me:
* Description: Get the user profile.
* Authentication: Bearer token (JWT) required in the Authorization header.
* Response:
json
```
{
  "user": 
  {"name": "John Doe",
  "email": "john@example.com",
  "zip_code": 98029,
  "tennis_level": 4.5,
  "preferences" : "Play during the morning"}
}
```
* PATCH /users/me
* Description: Update the user profile.
* Authentication: Bearer token (JWT) required in the Authorization header.
* Request Body:
```
{
  "name": "John Doe"
}
```
* Response:
json
```
{
  "user": 
  {"name": "John Doe",
  "email": "john@example.com",
  "zip_code": 98029,
  "tennis_level": 4.5,
  "preferences" : "Play during the morning"}
}
```
* DELETE /users/me
* Description: Delete the user profile.
* Authentication: Bearer token (JWT) required in the Authorization header.
* Response:
```
{"details": f'User {auth_user_id} deleted successfully!'}
```
Public route:
* GET /search
* Description: Get list of registered users.
* Request body:
json
```
{
  "zip_code": 98029,
  "tennis_level": 4.5,
}
```
* Response: 
```
[
  {"name": "John Doe",
  "email": "john@example.com",
  "zip_code": 98029,
  "tennis_level": 4.5,
  "preferences" : "Play during the morning"}
]
```
## Database Schema

Tennis Buddy uses SQL database (Postgres). Schema:

    tennis_user_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    auth_user_id = db.Column(db.String)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    tennis_level = db.Column(db.Float)
    preferences = db.Column(db.String(300))

## Authentication and Authorization
The API uses JWT for authentication. Users obtain a JWT after successful login, which they need to include in the Authorization header for authenticated endpoints.

## Deployment
Render - Postgres database on Render. 


from flask import Flask, jsonify, abort, make_response, request, render_template
from flask_sqlalchemy import SQLAlchemy

from typing import Any
from models import connect_to_db, db, User, Group

# Required to use Flask sessions and the debug toolbar
# app.secret_key = "security"


app = Flask(__name__)

## This is here to connect to the db first before quering or making changes to the db - 
## if this is not here you will get an strange error 'SQLALCHEMY_TRACK_MODIFICATIONS'
connect_to_db(app)


@app.route('/')
def hello():
    return render_template('index.html')

def scim_error(message, status_code=500):
    response = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
        "detail": message,
        "status": str(status_code)
    }
    return jsonify(response), status_code

# work on this last!
# @app.route('/scim/v2/Users', methods=['GET'])
#"""Get SCIM Users"""
# def get_user():
#     user = User.query.get(userName)
    
#     # count the number of user with the given email should be 1
#     # return that count with the following response:

#     {
#     "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
#     "totalResults": 0,
#     "startIndex": 1,
#     "itemsPerPage": 0,
#     "Resources": []
#     }


#     if not user:
#         return scim_error("User not found", 404)

    
@app.route('/scim/v2/Users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    """Get User With UID"""
    try:
        user = User.query.filter_by(id=user_id).one()
        # user = User.query.get(user_id)
    except:
        return scim_error("User not found", 404)
    return jsonify(user.scim_response())


@app.route('/scim/v2/Users', methods=['POST'])
def create_user():
    """Create User"""
    user_resource = request.get_json(force=True)
    print(user_resource)
    active = request.json.get("active")
    displayName = request.json.get("displayName")
    emails = request.json.get("emails")
    externalId = request.json.get("externalId")
    groups = request.json.get("groups")
    locale = request.json.get("locale")
    givenName = request.json["name"].get("givenName")
    middleName = request.json["name"].get("middleName")
    familyName = request.json["name"].get("familyName")
    password = request.json.get("password")
    schemas = request.json.get("schemas")
    userName = request.json.get("userName")
    
    # check if user already in datbase
    user_exists = User.query.filter_by(userName=userName).first()
    
    if user_exists:
        return scim_error("User already exists in the database.", 409)
    
    else:
        try:
            new_user = User(
            active=active,
            displayName=displayName,
            emails_primary=emails[0]["primary"],
            emails_value=emails[0]["value"],
            emails_type=emails[0]["type"],
            externalId=externalId,
            locale=locale,
            givenName=givenName,
            middleName=middleName,
            familyName=familyName,
            password=password,
            userName=userName,
        )
            db.session.add(new_user)
            print("new user created")
            # if groups:
            #     for group in groups:
            #             print(group)
            #             existing_group = Group.query.get(group["value"])
            #             if existing_group:
            #                 existing_group.users.append(user)
            #             else:
            #                 new_group = Group(displayName=group["displayName"])
            #                 db.session.add(new_group)
            #                 new_group.users.append(user)

            db.session.commit()
            print("user committed")
            return jsonify(new_user.scim_response()), 201
            print("hello")

        except Exception as e:
            return str(e)
            

@app.route('/scim/v2/Users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update SCIM User"""
    user = User.query.filter_by(id=user_id).one()
    if not user:
        return scim_error("User not found", 404)
    else:
        user.groups = request.json.get("groups")
        user.active = request.json.get("active")
        user.displayName = request.json.get("displayName")
        user.emails = request.json.get("emails")
        user.externalId = request.json.get("externalId")
        user.locale = request.json.get("locale")
        user.name = request.json.get("name")
        user.familyName = request.json["name"].get("familyName")
        user.middleName = request.json["name"].get("middleName")
        user.givenName = request.json["name"].get("givenName")
        user.password = request.json.get("password")
        user.schemas = request.json.get("schemas")
        user.userName = request.json.get("userName")

        db.session.commit()
        return jsonify(user.scim_response()), 200

@app.route('/scim/v2/Users/<string:user_id>', methods=['PATCH'])
def deactivate_user(user_id):
    """Deactivate SCIM User"""
    user = User.query.filter_by(id=user_id).one()
    if not user:
        return scim_error("User not found", 404)
    else:
        is_user_active = request.json["Operations"][0]["value"]["active"]
        user.active = is_user_active
        db.session.commit()
        return jsonify(""), 204

#@app.route('/scim/v2/Groups', methods=['GET'])
# def get_groups(group_id):
#     """Get Group With UID"""\
#     group = Group.query.filter_by(id=group_id).one()
#         return scim_error("Group not found", 404)
#     return jsonify(group.scim_response())

@app.route('/scim/v2/Groups/<string:group_id>', methods=['GET'])
def get_group(group_id):
    """Get Group With UID"""
    try:
        group = Group.query.filter_by(id=group_id).one()
    except:
        return scim_error("Group not found", 404)
    return jsonify(group.scim_response())

@app.route('/scim/v2/Groups', methods=['POST'])
def create_group():
    """Create Group"""
    group_resource = request.get_json(force=True)
    print(group_resource)
    displayName = request.json.get("displayName")
    print(displayName)
    members = request.json.get("members")

    # check if group already in datbase
    group_exists = Group.query.filter_by(displayName=displayName)
    print(group_exists)
    if group_exists:
        return scim_error("Group already exists in the database.", 409)
    else:
        new_group = Group(
        displayName=displayName,
        members=members,
    )
        db.session.add(new_group)
        print("group created")
        db.session.commit()
        print("group committed")
        return jsonify(new_group.scim_response()), 201

if __name__ == "__main__":

    # Turn on debugger only for testing app
    #app.debug = True
    app.run(debug=True)
    connect_to_db(app) # needed could not connect to server if running from terminal
    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    #app.run(host="0.0.0.0")




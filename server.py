
from flask import Flask, jsonify, abort, make_response, request, render_template
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from models import connect_to_db, db, User


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
# app.secret_key = "security"

@app.route('/')
def hello():
    return render_template('index.html')

## Example call to make sure the route works
@app.route('/scim/v2/User', methods=['GET'])
def users_post():
    response = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": "test",
            "userName": "test",
            "name": {
                "familyName": "test",
                "givenName": "test",
                "middleName": "test",
            },
            "active": "test",
            "meta": {
                "resourceType": "User",
                "location": "test",
            }
        }
    return jsonify(response)


def scim_error(message, status_code=500):
    rv = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
        "detail": message,
        "status": str(status_code)
    }
    return jsonify(rv), status_code

@app.route('/scim/v2/Users/', methods=['GET'])


@app.route('/scim/v2/Users/<string:user_id>', methods=['GET'])
def user_get(user_id):
    try:
        #user = User.query.filter_by(id=user_id).one()
        user = User.query.get(user_id)
    except:
        return scim_error("User not found", 404)
    return jsonify(user)

# @app.route('/scim/v2/Users', methods=['POST'])
# @app.route('/scim/v2/Users/{{userId}}', methods=['PUT'])
# @app.route('/scim/v2/Users/{{userId}}', methods=['PATCH'])
# @app.route('/scim/v2/Groups', methods=['GET'])
# @app.route('/scim/v2/Groups/{{groupId}}', methods=['GET'])
# @app.route('/scim/v2/Groups', methods=['POST'])


if __name__ == "__main__":

    
    # Turn on debugger only for testing app
    #app.debug = True
    app.run(debug=True)
    connect_to_db(app) # was missing! could not connect to server
    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    #app.run(host="0.0.0.0")




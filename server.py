
from flask import Flask
import flask
from flask import render_template

app = Flask(__name__)
database_url = os.getenv('DATABASE_URL', 'sqlite:///test-users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return 'Hello, World!'




class ListResponse():
    def __init__(self, list, start_index=1, count=None, total_results=0):
        self.list = list
        self.start_index = start_index
        self.count = count
        self.total_results = total_results

## has a method called to_scim_resource not the same as the method under user. rv = render view?
    def to_scim_resource(self):
        rv = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "totalResults": self.total_results,
            "startIndex": self.start_index,
            "Resources": []
        }
        resources = []
        for item in self.list:
            resources.append(item.to_scim_resource())
        if self.count:
            rv['itemsPerPage'] = self.count #add another attribute to the main rv list = itemsPerPage
        rv['Resources'] = resources
        return rv

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True)
    active = db.Column(db.Boolean, default=False)
    userName = db.Column(db.String(250),
                         unique=True,
                         nullable=False,
                         index=True)
    familyName = db.Column(db.String(250))
    middleName = db.Column(db.String(250))
    givenName = db.Column(db.String(250))


@app.route('/scim/v2/Users', methods=['GET'])


## Example call to make sure the route works
@app.route('/scim/v2/Use', methods=['GET'])
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
    return flask.jsonify(response)



if __name__ == "__main__":
    app.run(debug=True)

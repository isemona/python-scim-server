"""Models and database functions."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.dialects.postgresql import UUID
import uuid

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

# Define a many-to-many relationship
links = db.Table(
    "link",
    db.Column(
        "group_id", UUID(as_uuid=True), db.ForeignKey("groups.id"), primary_key=True
    ),
    db.Column(
        "user_id", UUID(as_uuid=True), db.ForeignKey("users.id"), primary_key=True
    ),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    active = db.Column(db.Boolean)
    userName = db.Column(db.String())
    givenName = db.Column(db.String())
    middleName = db.Column(db.String())
    familyName = db.Column(db.String())
    groups = db.relationship(
        "Group",
        secondary=links,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )
    emails_primary = db.Column(db.Boolean)
    emails_value = db.Column(db.String())
    emails_type = db.Column(db.String())
    displayName = db.Column(db.String())
    locale = db.Column(db.String())
    externalId = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(
        self,
        active,
        userName,
        givenName,
        middleName,
        familyName,
        emails_primary,
        emails_value,
        emails_type,
        displayName,
        locale,
        externalId,
        password,
    ):
        self.active = active
        self.userName = userName
        self.givenName = givenName
        self.middleName = middleName
        self.familyName = familyName
        self.emails_primary = emails_primary
        self.emails_value = emails_value
        self.emails_type = emails_type
        self.displayName = displayName
        self.locale = locale
        self.externalId = externalId
        self.password = password

    def __repr__(self):
        return "<id {}>".format(self.id)

    def scim_response(self):
        groups = []
        for group in self.groups:
            groups.append({"display": group.displayName, "value": group.id})

        return {
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:User",
            ],
            "id": self.id,
            "userName": self.userName,
            "name": {
                "givenName": self.givenName,
                "middleName": self.middleName,
                "familyName": self.familyName,
            },
            "emails": [
                {
                    "primary": self.emails_primary,
                    "value": self.emails_value,
                    "type": self.emails_type,
                }
            ],
            "displayName": self.displayName,
            "locale": self.locale,
            "externalId": self.externalId,
            "active": self.active,
            "groups": groups,
            "meta": {"resourceType": "User"},
        }


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    displayName = db.Column(db.String())

    def scim_response(self):
        users = []
        for user in self.users:
            users.append({"display": user.userName, "value": user.id})

        return {
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:Group",
            ],
            "id": self.id,
            "meta": {
                "resourceType": "Group",
            },
            "displayName": self.displayName,
            "members": users,
        }

#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Okta123$@localhost:5432/database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.
    from server import app
    connect_to_db(app)

    # you specified db.create_all() here to create the database no need to type this command on the terminal
    db.create_all()

    print("Connected to DB.")
from models import connect_to_db, db, User, Group
from server import app

active = True
userName = "test.user@okta.local"
givenName = "Test"
middleName = ""
familyName = "User"
emails_primary = True
emails_value = "test.user@okta.local"
emails_type = "test.user@okta.local"
displayName = "Test User"
locale = "en-US"
externalId = "00ujl29u0le5T6Aj10h7"
password = '123'
displayName = 'Group 0'


def load_users():
    """Load users from Faker Library to database"""

    user = User(active = active,
        userName = userName,
        givenName = givenName,
        middleName = middleName,
        familyName = familyName,
        emails_primary = emails_primary,
        emails_value = emails_value,
        emails_type = emails_type,
        displayName = displayName,
        locale = locale,
        externalId = externalId,
        password = password,
        
                )
    # We need to add to the session or it won't ever be stored
    db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()

def load_groups():
    group = Group(displayName = displayName)
    db.session.add(group)
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    load_users()  
    load_groups()
    print("user and groups loaded.")
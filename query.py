from models import *

def create_user():
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

        db.session.add(user)
        db.session.commit()
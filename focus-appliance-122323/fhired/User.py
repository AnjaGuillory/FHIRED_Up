from flask.ext.login import UserMixin
import hashlib
# Basic Hash 256 ( No Secure enough for real app, desired (HMAC + SALT) )
user_database = {"aburgos": "f920cd4628136d5cef595ba8d629758b6d6e96463f64afe1407309d0be0cd361",
                 "FHIRedUp" : "96f53082968e609425115b8ac6b8899f239a4c57e4a338c46c466c29bf16a817" # PjV7kGTD
                }


class User(UserMixin):

    def __init__(self, username, password):
        self.id = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.id

    @classmethod
    def get(cls, id):
        return query_user(id)


def query_user(username):
    return User(username, user_database[username])


def auth(username, password):
    if username in user_database:
        if user_database[username] == hashlib.sha256(password).hexdigest():
            return query_user(username)

    return None

from google.appengine.ext import db


class SampleModel(db.Model):
    """
    A sample model demonstrating how to use Google DataStore
    """
    name = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)


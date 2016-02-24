from google.appengine.ext import db


class SampleModel(db.model):
    """
    A sample model demonstrating how to use Google DataStore
    """
    name = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
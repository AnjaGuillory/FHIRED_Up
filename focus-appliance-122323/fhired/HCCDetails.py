from google.appengine.ext import db


class HCCDetails(db.Model):
    pt_id = db.IntegerProperty(required=True)
    hcc = db.IntegerProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty(required=True, choices={"confirm", "provisional", "differential", "refuted", "entered_error", "unknown"})
    snow_med_codes = db.StringListProperty(required=True)
    notes = db.TextProperty()

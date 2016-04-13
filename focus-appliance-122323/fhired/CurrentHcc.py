from google.appengine.ext import db
from Entities import *


class CurrentHcc(db.Model):
    pt_id = db.IntegerProperty(required=True)
    hcc = db.IntegerProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty(required=True, choices={"confirm", "provisional", "differential", "refuted", "entered_error", "unknown"})
    snow_med_codes = db.StringListProperty(required=True)
    notes = db.TextProperty()

    def get_hcc(self):
        hcc_details = SnowmedConverter.get_hcc_details(self.hcc)
        return Hcc(self.hcc, self.created.year, hcc_details[1], hcc_details[2], self.notes)

    @classmethod
    def get_all_by(cls, attr, value):
        q = CurrentHcc.all()
        q.filter(attr+" =", value)
        return q.fetch(1000)

    @classmethod
    def exits(cls, patient_id, hcc):
        q = CurrentHcc.all()
        q.filter("pt_id =", patient_id)
        q.filter("hcc =", hcc)
        if q.count() > 0:
            return True
        return False

    @classmethod
    def get_by(cls, patient_id, hcc):
        q = CurrentHcc.all()
        q.filter("pt_id =", patient_id)
        q.filter("hcc =", hcc)
        return q.get()


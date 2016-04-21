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
    def empty(cls, pt_id, hcc, snow_med_codes):
        return CurrentHcc(pt_id=pt_id, hcc=hcc, snow_med_codes=snow_med_codes, status="confirm")

    @classmethod
    def get_all_by(cls, attr, value, include_rejected):
        q = CurrentHcc.all()
        q.filter(attr+" =", value)
        if not include_rejected:
            q.filter("status =", "confirm")

        return q.fetch(1000)

    @classmethod
    def exits(cls, pt_id, hcc):
        q = CurrentHcc.all()
        q.filter("pt_id =", pt_id)

        if hcc is not None:
            q.filter("hcc =", hcc)

        total = q.count()
        if total > 0:
            return True
        return False

    @classmethod
    def get_by(cls, pt_id, hcc):
        q = CurrentHcc.all()
        q.filter("pt_id =", pt_id)
        q.filter("hcc =", hcc)
        return q.get()

    @classmethod
    def delete_by(cls, pt_id, hcc):
        success = False
        q = CurrentHcc.all()
        q.filter("pt_id =", pt_id)
        q.filter("hcc =", hcc)

        for obj in q.fetch(1000):
            success = obj.delete()
        return success




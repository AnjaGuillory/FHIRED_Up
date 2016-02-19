from google.appengine.ext import db
from models import SampleModel


class Store:

    def store_sample(self, name):
        sample = SampleModel(name=name)
        sample.put()

    def get_sample(self, name):
        query = SampleModel.all().filter('name', name)
        return query.fetch(1)

    def remove_sample(self, name):
        query = SampleModel.gql('WHERE name = :1', name)
        return self._delete_first()

    def _delete_first(self, query):
        """Deletes the first result for the given query.
        Returns True if an entity was deleted, false if no entity could be deleted
        or if the query returned no results.
        """
        results = query.fetch(1)

        if results:
          try:
            results[0].delete()
            return True
          except db.Error:
            return False
        else:
          return False
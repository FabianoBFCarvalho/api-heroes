from fireo.models import Model
from fireo.fields import TextField, DateTime, IDField
from datetime import datetime


class Hero(Model):
    """Model Hero"""
    id = IDField()
    description = TextField()
    image_url = TextField()
    name = TextField()
    universe = TextField()

    class Meta:
        collection_name = "Hero"

    @classmethod
    def all(cls, cursor=None, list_type='cursor'):
        """
        Get all heroes
        :param int limit: limit of heroes
        :return: Heroes list
        """
        if list_type == 'all':
            limit = 100
        else:
            limit = 20

        if cursor:
            return cls.collection.cursor(cursor).fetch(limit)
        else:
            return cls.collection.fetch(limit)

    @classmethod
    def get_by_id(cls, hero_id):
        """
        Get by id
        :param hero_id:
        :return:
        """
        return cls.collection.get('Hero/%s' % hero_id)

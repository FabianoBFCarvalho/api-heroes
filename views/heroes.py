from models.hero import Hero
from modules.heroes import HeroesModule
from flask import request
from flask.views import MethodView
import logging
import json


class HeroesHandler(MethodView):
    """"""

    def get(self):
        """"""
        cursor = request.args.get('cursor')
        list_type = request.args.get('list_type') or 'cursor'

        heroes = Hero.all(cursor=cursor, list_type=list_type)
        heroes_json = []
        for hero in heroes:
            heroes_json.append(hero.to_dict())

        return {
            'heroes': heroes_json,
            'cursor': heroes.cursor if len(heroes_json) == 20 else ''
        }

    def post(self):
        """"""
        try:
            params = self.dict_data()
            if 'hero' not in params:
                return {'error': str('parameter hero not found')}, 400
            return HeroesModule.create(params.get('hero'))

        except Exception as error:
            return {'error': str(error)}, 500

    def dict_data(self):
        """
        Get data in json format
        :return dict: Dict data
        """
        try:
            return json.loads(request.data)
        except Exception as error:
            logging.warning('Error on loads json')
            logging.warning(error)
            return {}


class HeroHandler(MethodView):
    """"""
    def get(self, id):
        """"""
        try:
            return Hero.get_by_id(id).to_dict()
        except Exception as error:
            return {'error': str(error)}, 500

    def post(self, id):
        """"""
        try:
            params = self.dict_data()
            if 'hero' not in params:
                return {'error': str('parameter hero not found')}, 400
            hero = Hero.get_by_id(id)
            if not hero:
                return {'error': str('hero not found')}, 404

            return HeroesModule.update(hero, params.get('hero'))
        except Exception as error:
            return {'error': str(error)}, 500

    def delete(self, id):
        """"""
        try:
            hero = Hero.get_by_id(id)
            if not hero:
                return {'error': str('hero not found')}, 404

            Hero.collection.delete('Hero/%s' % id)

            return {'success': 'deleted'}, 200
        except Exception as error:
            return {'error': str(error)}, 500

    def dict_data(self):
        """
        Get data in json format
        :return dict: Dict data
        """
        try:
            return json.loads(request.data)
        except Exception as error:
            logging.warning('Error on loads json')
            logging.warning(error)
            return {}

class TopHeroesHandler(MethodView):
    """"""
    def get(self):
        """"""
        try:
            import random
            heroes = Hero.all(list_type='all')
            heroes_json = []
            for hero in heroes:
                heroes_json.append(hero.to_dict())
            random.shuffle(heroes_json)
            return {'heroes': heroes_json[0:6]}

        except Exception as error:
            return {'error': str(error)}, 500

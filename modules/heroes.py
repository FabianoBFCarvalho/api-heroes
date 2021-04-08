from models.hero import Hero
import re


class HeroesModule(object):
    """"""
    @classmethod
    def create(cls, params):
        """"""
        if not params.get('name'):
            return {'error': str('name is required')}, 400
        if not params.get('universe'):
            return {'error': str('universe is required')}, 400

        hero = Hero()
        hero.name = cls.title_case(params.get('name'))
        hero.image_url = cls.title_case(params.get('imageUrl'))
        hero.description = cls.title_case(params.get('description'))
        hero.universe = cls.title_case(params.get('universe'))
        hero.save()

        return hero.to_dict()

    @classmethod
    def update(cls, hero, params):
        """"""
        if not params.get('name'):
            return {'error': str('name is required')}, 400
        if not params.get('universe'):
            return {'error': str('universe is required')}, 400
        hero.name = cls.title_case(params.get('name'))
        hero.image_url = cls.title_case(params.get('imageUrl'))
        hero.description = cls.title_case(params.get('description'))
        hero.universe = cls.title_case(params.get('universe'))
        hero.save()

        return hero.to_dict()

    def title_case(value, exceptions=None):
        """
        Get text in title case
        :param str value: Value
        :param list of str exceptions: List of words to except title case
        :return str: Text in title case
        """
        if not value:
            return value
        if not exceptions:
            exceptions = ['e', 'da', 'de', 'do', 'das', 'dos']
        value_list = re.split(' ', value)
        formatted_value = [value_list[0].capitalize()]
        for word in value_list[1:]:
            try:
                exception_index = exceptions.index(word.lower())
            except:
                exception_index = -1
            if exception_index >= 0:
                formatted_value.append(exceptions[exception_index])
            else:
                formatted_value.append(
                    word.capitalize() if not word.isupper() else word)
        return " ".join(formatted_value)
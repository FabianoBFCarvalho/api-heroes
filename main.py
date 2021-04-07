import logging

import fireo
from flask import request, Flask
from flask_cors import CORS
from flask_restful import Resource, Api

from views.heroes import HeroesHandler, HeroHandler, TopHeroesHandler

app = Flask(__name__)
CORS(app)
API = Api(app)

fireo.connection(
        from_file='./api-heroes-51e3b-firebase-adminsdk-ika07-67ab2b50f9.json')


@app.before_request
def start_request():
    """Start api request"""
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.DEBUG)
    if request.method == 'OPTIONS':
        return '', 200
    if not request.endpoint:
        return 'Sorry, Nothing at this URL.', 404


class Index(Resource):
    """ class return API index """
    @staticmethod
    def get():
        """ return API initial JSON """
        return {"API": "HEROES API"}


API.add_resource(Index, '/', endpoint='index')
API.add_resource(HeroesHandler, '/heroes', endpoint='heroes')
API.add_resource(HeroHandler, '/hero/<id>', endpoint='hero')
API.add_resource(TopHeroesHandler, '/top-heroes', endpoint='top-heroes')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
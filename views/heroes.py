from models.hero import Hero
from modules.heroes import HeroesModule
from flask import request
from flask.views import MethodView
import logging
import json


class DocumentationHandler(MethodView):
    """"""

    def get(self):
        return {
      "swagger": "2.0",
      "info": {
        "description": "Hero API",
        "version": "1.0.0",
        "title": "Hero API",
        "termsOfService": "http://swagger.io/terms/",
        "contact": {
          "email": "bruno-chikuji@hotmail.com"
        },
        "license": {
          "name": "Apache 2.0",
          "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        }
      },
      "host": "api-default-309921.rj.r.appspot.com",
      "basePath": "/",
      "schemes": [
        "https",
        "http"
      ],
      "paths": {
        "/heroes": {
          "post": {
            "tags": [
              "Hero"
            ],
            "summary": "Add new hero",
            "description": "",
            "operationId": "addHero",
            "consumes": [
              "application/json"
            ],
            "produces": [
              "application/json"
            ],
            "parameters": [
              {
                "in": "body",
                "name": "body",
                "description": "Hero json",
                "required": True,
                "schema": {
                  "type": "object",
                  "properties": {
                    "hero": {
                      "$ref": "#/definitions/Hero"
                    }
                  }
                }
              }
            ],
            "responses": {
              "400": {
                "description": "Bad request"
              }
            }
          },
          "get": {
            "tags": [
              "Hero"
            ],
            "summary": "Get heroes list",
            "description": "",
            "operationId": "getHeroes",
            "produces": [
              "application/json"
            ],
            "responses": {
              "200": {
                "description": "successful operation",
                "schema": {
                  "type": "object",
                  "properties": {
                    "heroes": {
                      "type": "array",
                      "items": {
                        "$ref": "#/definitions/Hero"
                      }
                    },
                    "cursor": {
                      "type": "string",
                      "example": "drfwegfdgdfgdfhgdf"
                    }
                  }
                }
              },
              "400": {
                "description": "Invalid ID supplied"
              },
              "404": {
                "description": "Hero not found"
              },
              "405": {
                "description": "Validation exception"
              }
            }
          }
        },
        "/hero/{heroId}": {
          "get": {
            "tags": [
              "Hero"
            ],
            "summary": "Find hero by ID",
            "description": "Returns a single hero",
            "operationId": "getHeroById",
            "produces": [
              "application/json"
            ],
            "parameters": [
              {
                "name": "heroId",
                "in": "path",
                "description": "ID of hero to return",
                "required": True,
                "type": "string"
              }
            ],
            "responses": {
              "200": {
                "description": "successful operation",
                "schema": {
                  "$ref": "#/definitions/Hero"
                }
              },
              "400": {
                "description": "Invalid ID supplied"
              },
              "404": {
                "description": "Hero not found"
              }
            }
          },
          "post": {
            "tags": [
              "Hero"
            ],
            "summary": "Updates a hero",
            "description": "",
            "operationId": "updateHero",
            "consumes": [
              "application/json"
            ],
            "produces": [
              "application/json"
            ],
            "parameters": [
              {
                "name": "heroId",
                "in": "path",
                "description": "ID of hero that needs to be updated",
                "required": True,
                "type": "string"
              },
              {
                "in": "body",
                "name": "body",
                "description": "Hero json",
                "required": True,
                "schema": {
                  "type": "object",
                  "properties": {
                    "hero": {
                      "$ref": "#/definitions/Hero"
                    }
                  }
                }
              }
            ],
            "responses": {
              "405": {
                "description": "Invalid input"
              }
            }
          },
          "delete": {
            "tags": [
              "Hero"
            ],
            "summary": "Deletes a hero",
            "description": "",
            "operationId": "deleteHero",
            "produces": [
              "application/json"
            ],
            "parameters": [
              {
                "name": "heroId",
                "in": "path",
                "description": "Hero id to delete",
                "required": True,
                "type": "string"
              }
            ],
            "responses": {
              "400": {
                "description": "Invalid ID supplied"
              },
              "404": {
                "description": "Hero not found"
              }
            }
          }
        }
      },
      "definitions": {
        "Hero": {
          "type": "object",
          "required": [
            "name",
            "universe"
          ],
          "properties": {
            "id": {
              "type": "string",
              "example": "fsertsdgfdg"
            },
            "name": {
              "type": "string",
              "example": "Flash"
            },
            "imageUrl": {
              "type": "string",
              "example": "https://teste.com.br/image.jpg"
            },
            "description": {
              "type": "string",
              "example": "Description"
            },
            "universe": {
              "type": "string",
              "description": "Universe",
              "enum": [
                "dc",
                "marvel"
              ]
            }
          },
          "xml": {
            "name": "Hero"
          }
        }
      },
      "externalDocs": {
        "description": "Find out more about Swagger",
        "url": "http://swagger.io"
      }
    }


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

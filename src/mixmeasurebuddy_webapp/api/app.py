import json

from flask import Flask, jsonify, make_response, Blueprint, redirect
from dotenv import load_dotenv
import os
from pathlib import Path
from flask_swagger_generator.components import SwaggerVersion
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger_generator.generators import Generator
import logging
from configparser import ConfigParser
import pymongo
import mongoengine
import names
# IMPORT CUSTOM DATABASE MODELS
import dbmodels

logging.getLogger().setLevel(logging.DEBUG)
load_dotenv() # LOAD .env

config = ConfigParser()
config.read(Path.joinpath(Path(__file__).parent, Path("config.cfg")))

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
SWAGGERFILE_PATH = 'static/swagger.yaml'
SWAGGERFILE_PATH_ABS = Path.joinpath(Path(__file__).parent, Path(SWAGGERFILE_PATH))

# Create the bluepints
blueprint = Blueprint(config.get('GENERAL', 'APP_NAME') + '-API', __name__)
# Create the flask app
app = Flask(__name__)
# LOAD CONFIG

# SETUP MONFO

# Create swagger version 3.0 generator
generator = Generator.of(SwaggerVersion.VERSION_THREE)
# Call factory function to create our blueprint
app.register_blueprint(get_swaggerui_blueprint(SWAGGER_URL, "/" + SWAGGERFILE_PATH,config={'app_name': "MixMeasureBuddy-API"}))



@blueprint.route('/api/mmb/', methods=['GET'])
def mmbd_index(mmb_device_id: str):  # mixmeasurebuddy.com/api/ system_id / recipes.json
    return make_response(jsonify({'mmbd_recipes': '/api/mmb/<string:mmb_device_id>', 'mmbd_recipe': '/api/mmb/<string:mmb_device_id>/<string:recipe_id>'}), 200)





# ["resipe_file_uri_relative"]
@generator.response(status_code=200, schema={'id': 10, 'name': 'test_object'})
@blueprint.route('/api/mmb/<string:mmb_device_id>/recipes', methods=['GET'])
def mmbd_recipes(mmb_device_id: str):  # mixmeasurebuddy.com/api/ system_id / recipes.json

    # CREATE USER IF NOT PRESENT

    if len(dbmodels.Users.objects(linked_device_id=mmb_device_id)) <= 0:
        user = dbmodels.Users(name="", linked_device_id=mmb_device_id)
        user.save()


    data: list = [
        "Tequila_Sunrise",
    ]
    return make_response(jsonify(data), 200)

@generator.response(status_code=200, schema={'recipe': {'name': 'Tequila_Sunrise', 'description': 'recipe text','version': '1.0.0','ingredients': {'0': 'name'},'steps':[{'action':'scale', 'ingredient':'0', 'amount':720},{'action':'confirm', 'text':'press ok'}]}, 'name': 'Recipe_Name'})
@blueprint.route('/api/mmb/<string:mmb_device_id>/recipe/<string:recipe_id>', methods=['GET'])
def mmbd_recipe(mmb_device_id: str, recipe_id: str):

    # TODO ON RP2040 CHECK FOR VALID RESULT
    # CREATE USER IF NOT PRESENT
    if len(dbmodels.Users.objects(linked_device_id=mmb_device_id)) <= 0:
        user = dbmodels.Users(name="", linked_device_id=mmb_device_id)
        user.save()





    data: dict = {


    }
    return make_response(jsonify(data), 200)





@blueprint.route('/api')
def api():
    return redirect(SWAGGER_URL)

@blueprint.route('/')
def index():
    return redirect('/api')

app.register_blueprint(blueprint)
generator.generate_swagger(app, destination_path=SWAGGERFILE_PATH)

if __name__ == "__main__":
    # CHECK DB CONNECTION
    DATABASE_CONNECTION_STRING: str = os.environ.get("DATABASE_CONNECTION_STRING", "mongodb://mongo:27017")
    DB_NAME: str = os.environ.get("MMB_DATABASE_NAME", "mixmeasurebuddy")
    DB_COLLECTION_RECIPES: str = "recipes"
    DB_COLLECTION_USERS: str = "users"
    DB_COLLECTION_INGREDIENTS: str = "ingredients"

    # PREPARE DATABASE
    # WE ARE USING PYMONGO TO CHECK THE DATABASE
    db: pymongo.MongoClient = pymongo.MongoClient(DATABASE_CONNECTION_STRING)
    # CREATE DATABASE
    dblist = db.list_database_names()

    if DB_NAME in dblist:
        logging.debug("The MMB_DATABASE {} exists.".format(DB_NAME))
    mmb_database = db[DB_NAME]
    # CREATE COLLECTIONS
    target_collections = [DB_COLLECTION_RECIPES, DB_COLLECTION_USERS, DB_COLLECTION_INGREDIENTS]
    existing_collections = mmb_database.list_collection_names()
    for collection in target_collections:
        if collection in existing_collections:
            logging.debug("The collection {} exists.".format(collection))
        else:
            mmb_database.create_collection(collection)
    # FINALLY CLOSE CONNECTION
    db.close()


    # CREATE mongoengine CONNECTION
    cs = "{}/{}".format(DATABASE_CONNECTION_STRING, DB_NAME)
    logging.debug(cs)


    mongoengine.connect(host=cs)



    test_ing = [
        "Pineapple-Juice",
        "Cream",
        "white Rum",
        "Crushed Ice",
        "Coconut-Juice",
        "Strawberries",
        "white Tequila",
        "Grenadine",
        "Orange-Juice"
    ]

    for i in test_ing:
        if len(dbmodels.Ingredient.objects(name=i)) <= 0:
            r = dbmodels.Ingredient()
            r.name = i
            r.save()

    if len(dbmodels.Recipe.objects(name="Tequila Sunrise")) <= 0:
        i1 = dbmodels.Ingredient.objects(name="white Tequila")

        r = dbmodels.Recipe()
        r.name = "Tequila Sunrise"
        r.description = "A nice Tequila Sunrise Cocktail"
        r.ingredients = [i1[0]]
        r.steps = [dbmodels.Step(amount=10, action="scale", ingredient=[i1])]
        r.save()

    #    r1.ingredients["0"] = "10 Strawberries"

        #r1.steps = [dbmodels.Step(text="puree strawberries", action="confirm")]

        #r1.save()
    # START FLASK
    app.run(host=os.environ.get("API_SERVER_BIND_ADDR", '0.0.0.0'), port=os.environ.get("API_SERVER_PORT", 5000), debug=True)

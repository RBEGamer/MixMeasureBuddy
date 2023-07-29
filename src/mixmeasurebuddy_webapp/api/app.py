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





@blueprint.route('/api/mmb/<string:mmb_device_id>/register', methods=['GET'])
def mmbd_register(mmb_device_id: str):  # mixmeasurebuddy.com/api/ system_id / recipes.json
    # CHECK USER ALREADY EXISTS
    if len(dbmodels.Users.objects(linked_device_id=mmb_device_id)) > 0:
        return make_response(jsonify({}), 200)

    # CREATE NEW USER
    new_user = dbmodels.Users(name=names.get_full_name(), linked_device_id=mmb_device_id)
    # LINK SOME RECIPES FOR GETTING STARTED
    new_user.linked_recipes = dbmodels.Recipe.objects(default_recipe=True)
    # SAVE USER
    new_user.save()


    return make_response(jsonify({}), 200)


@generator.response(status_code=200, schema={'id': 10, 'name': 'test_object'})
@blueprint.route('/api/mmb/<string:mmb_device_id>/recipes', methods=['GET'])
def mmbd_recipes(mmb_device_id: str):  # mixmeasurebuddy.com/api/ system_id / recipes.json

    # CHECK DEVICE REGISTRATION
    users = dbmodels.Users.objects(linked_device_id=mmb_device_id)
    if len(dbmodels.Users.objects(linked_device_id=mmb_device_id)) <= 0:
        return make_response(jsonify({"err": "please register device"}), 401)

    user = users[0]
    linked_recipes = user.linked_recipes

    ret = []
    for r in linked_recipes:
        ret. append(r.name)

    return make_response(jsonify(ret), 200)





@generator.response(status_code=200, schema={'recipe': {'name': 'Tequila_Sunrise', 'description': 'recipe text','version': '1.0.0','ingredients': {'0': 'name'},'steps':[{'action':'scale', 'ingredient':'0', 'amount':720},{'action':'confirm', 'text':'press ok'}]}, 'name': 'Recipe_Name'})
@blueprint.route('/api/mmb/<string:mmb_device_id>/recipe/<string:recipe_id>', methods=['GET'])
def mmbd_recipe(mmb_device_id: str, recipe_id: str):
    # CHECK DEVICE REGISTRATION
    users = dbmodels.Users.objects(linked_device_id=mmb_device_id)
    if len(users) <= 0:
        return make_response(jsonify({"err": "please register device"}), 401)


    user_recipes = dbmodels.Users.objects.get(linked_device_id=mmb_device_id).linked_recipes
    global_recipes = dbmodels.Recipe.objects(name=recipe_id)
    if len(global_recipes) <= 0:
        return make_response(jsonify({}), 404)

    recipe = global_recipes[0]


    found = False
    for ur in user_recipes:
        if recipe.name in ur.name:
            found = True
            break
    if not found:
        return make_response(jsonify({}), 404)

    ret = {}
    # CONVERT DATA FROM DB TO JSON
    # SIMPLY TO SAVE SPACE FOR THE MICROCONTROLLERS
    ret['name'] = recipe.name
    ret['description'] = recipe.description
    ret['version'] = recipe.version
    # TODO REMOVE
    for c in recipe.category:
        ret['category'] = c.name
        break

    il = []
    for c in recipe.ingredients:
        il.append(str(c.name))
    ret['ingredients'] = il

    sl = []
    for c in recipe.steps:
        entry: dict = {
            'action': c.action,
        }

        if c.text:
            entry['text'] = c.text

        # CONVERT UNITS
        if c.ingredient:
            entry['ingredient'] = c.ingredient.name

        if c.amount:
            if c.ingredient and c.ingredient.weight_g_per_unit:
                entry['amount'] = float(c.amount) * float(c.ingredient.weight_g_per_unit)
            else:
                entry['amount'] = c.amount



        sl.append(entry)

    ret['steps'] = sl




    return make_response(jsonify(ret), 404)






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
    DB_COLLECTION_CATEGORIES: str = "categories"
    # PREPARE DATABASE
    # WE ARE USING PYMONGO TO CHECK THE DATABASE
    db: pymongo.MongoClient = pymongo.MongoClient(DATABASE_CONNECTION_STRING)
    # CREATE DATABASE
    dblist = db.list_database_names()

    if DB_NAME in dblist:
        logging.debug("The MMB_DATABASE {} exists.".format(DB_NAME))
    mmb_database = db[DB_NAME]
    # CREATE COLLECTIONS
    target_collections = [DB_COLLECTION_RECIPES, DB_COLLECTION_USERS, DB_COLLECTION_INGREDIENTS, DB_COLLECTION_CATEGORIES]
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

    # CREATE ADMIN USER
    if len(dbmodels.Users.objects(linked_device_id="1337")) <= 0:
        user = dbmodels.Users(name="MixMeasureBuddy Owner A")
        user.linked_device_id="1337"
        user.permissions = 1
        user.save()
    if len(dbmodels.Users.objects(linked_device_id="1338")) <= 0:
        user = dbmodels.Users(name="MixMeasureBuddy Owner B")
        user.linked_device_id="1338"
        user.permissions = 1
        user.save()


    # CREATE CATEGORY
    categories = ["Cocktails", "Virgin-Cocktails", "Longdrinks"]
    for c in categories:
        if len(dbmodels.Category.objects(name=c)) <= 0:
            dbmodels.Category(name=c).save()



    # CREATE  INGREDIENTS
    test_ing = ["Pineapple-Juice", "Cream", "white Rum", "Strawberry-Syrup","Malibu-Coconut", "Crushed Ice", "Coconut-Juice", "Strawberries", "white Tequila", "Grenadine", "Orange-Juice"]

    for i in test_ing:
        if len(dbmodels.Ingredient.objects(name=i)) <= 0:
            r = dbmodels.Ingredient(name=i).save()


    # CREATE TEST RECIPES
    if len(dbmodels.Recipe.objects(name="Tequila Sunrise")) <= 0:
        i_list = []
        i_list.append(dbmodels.Ingredient.objects(name="white Tequila")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Orange-Juice")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Grenadine")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Crushed Ice")[0])

        i_steps = []
        i_steps.append(dbmodels.Step(amount=20, action="scale", ingredient=dbmodels.Ingredient.objects(name="white Tequila")[0]))
        i_steps.append(dbmodels.Step(amount=40, action="scale",ingredient=dbmodels.Ingredient.objects(name="Grenadine")[0]))
        i_steps.append(dbmodels.Step(amount=110, action="scale", ingredient=dbmodels.Ingredient.objects(name="Orange-Juice")[0]))
        i_steps.append(dbmodels.Step(action="wait", text="MIX", amount=30))
        i_steps.append(dbmodels.Step(action="confirm", text="ADD ICE"))


        ra = dbmodels.Recipe()
        ra.name = "Tequila Sunrise"
        ra.category = dbmodels.Category.objects(name="Cocktails")
        ra.description = "A nice Tequila Sunrise Cocktail"
        ra.ingredients = i_list
        ra.default_recipe = True
        ra.author = dbmodels.Users.objects(linked_device_id="1337")[0]
        ra.steps = i_steps
        ra.save()



    if len(dbmodels.Recipe.objects(name="Pina Colada")) <= 0:
        i_list = []
        i_list.append(dbmodels.Ingredient.objects(name="Malibu-Coconut")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Strawberry-Syrup")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Pineapple-Juice")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Cream")[0])

        i_steps = []
        i_steps.append(dbmodels.Step(amount=40, action="scale", ingredient=dbmodels.Ingredient.objects(name="Malibu-Coconut")[0]))
        i_steps.append(dbmodels.Step(amount=40, action="scale", ingredient=dbmodels.Ingredient.objects(name="Strawberry-Syrup")[0]))
        i_steps.append(dbmodels.Step(amount=20, action="scale", ingredient=dbmodels.Ingredient.objects(name="Cream")[0]))
        i_steps.append(dbmodels.Step(amount=80, action="scale", ingredient=dbmodels.Ingredient.objects(name="Pineapple-Juice")[0]))


        rb = dbmodels.Recipe()
        rb.name = "Pina Colada"
        rb.category = dbmodels.Category.objects(name="Cocktails")
        rb.description = "One of the most popular tropical cocktails from the Caribbean is the Pina Colada, simply delicious with strawberries"
        rb.ingredients = i_list
        rb.default_recipe = True
        rb.author = dbmodels.Users.objects(linked_device_id="1338")[0]
        rb.steps = i_steps
        rb.save()


    # START FLASK
    app.run(host=os.environ.get("API_SERVER_BIND_ADDR", '0.0.0.0'), port=os.environ.get("API_SERVER_PORT", 5000), debug=True)

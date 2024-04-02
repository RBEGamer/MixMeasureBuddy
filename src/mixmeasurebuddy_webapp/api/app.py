import json

import bleach
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
import urllib.parse

from mongoengine import DEFAULT_CONNECTION_NAME, connect

# IMPORT CUSTOM DATABASE MODELS
import dbmodels
from flask import request

logging.getLogger().setLevel(logging.DEBUG)
load_dotenv()  # LOAD .env

config = ConfigParser()
config.read(Path.joinpath(Path(__file__).parent, Path("config.cfg")))

DATABASE_CONNECTION_STRING: str = os.environ.get("DATABASE_CONNECTION_STRING", "mongodb://mongo:27017")
DATABASE_NAME: str = os.environ.get("MMB_DATABASE_NAME", "mixmeasurebuddy")
DB_COLLECTION_RECIPES: str = "recipes"
DB_COLLECTION_USERS: str = "users"
DB_COLLECTION_INGREDIENTS: str = "ingredients"
DB_COLLECTION_CATEGORIES: str = "categories"

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
SWAGGERFILE_PATH = 'swagger.yaml'
SWAGGERFILE_PATH_ABS = Path.joinpath(Path(__file__).parent, Path(SWAGGERFILE_PATH))

# Create the bluepints
blueprint = Blueprint(config.get('GENERAL', 'APP_NAME') + '-API', __name__)
# Create the flask app
app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')

db = mongoengine

connect(DATABASE_NAME, host=DATABASE_CONNECTION_STRING, alias='default')

# db.connect('microblog') # connects to database named microblog
# LOAD CONFIG

# SETUP MONFO

# TODO sANTInITE ALL VAriabled
# Create swagger version 3.0 generator
generator = Generator.of(SwaggerVersion.VERSION_THREE)
# Call factory function to create our blueprint
app.register_blueprint(
    get_swaggerui_blueprint(SWAGGER_URL, "/" + SWAGGERFILE_PATH, config={'app_name': "MixMeasureBuddy-API"}))


@blueprint.route('/api/mmb/', methods=['GET'])
def mmbd_index(mmb_device_id: str):  # mixmeasurebuddy.com/api/ system_id / recipes.json
    mmb_device_id = bleach.clean(mmb_device_id)
    return make_response(jsonify({'mmbd_recipes': '/api/mmb/<string:mmb_device_id>',
                                  'mmbd_recipe': '/api/mmb/<string:mmb_device_id>/<string:recipe_id>'}), 200)


@app.route('/api/mmb/<string:mmb_device_id>', methods=['GET'])
def mmbd_manage_redirect(mmb_device_id: str):  # mixmeasurebuddy.com/api/ system_id / recipes.json
    mmb_device_id = bleach.clean(mmb_device_id)
    return redirect('/manage.html?mmb_device_id={}'.format(mmb_device_id))


@blueprint.route('/api/mmb/<string:mmb_device_id>/register', methods=['GET'])
def mmbd_register(mmb_device_id: str):  # mixmeasurebuddy.com/api/ system_id / recipes.json
    mmb_device_id = bleach.clean(mmb_device_id)
    # CHECK USER ALREADY EXISTS
    if len(dbmodels.Users.objects(linked_device_id=mmb_device_id)) > 0:
        return make_response(jsonify({}), 200)

    # CREATE NEW USER
    new_user = dbmodels.Users(name=names.get_full_name(), linked_device_id=mmb_device_id)
    # LINK SOME RECIPES FOR GETTING STARTED
    new_user.linked_recipes = dbmodels.Recipe.objects(default_recipe=True)

    # STORE ADDITIONAL INFORMATION ABOUT THE DEVICE IF PRESENT
    if 'DEVICE_FIRMWARE_VERSION' in request.headers:
        new_user.firmware_version = request.headers['DEVICE_FIRMWARE_VERSION']

    if 'DEVICE_HARDWARE_VERSION' in request.headers:
        new_user.hardwareversion = request.headers['DEVICE_HARDWARE_VERSION']

    # SAVE USER
    new_user.save()

    return make_response(jsonify({}), 200)


@generator.response(status_code=200, schema={'id': 10, 'name': 'test_object'})
@blueprint.route('/api/recipes', methods=['GET'])
def user_all_recipes():  # mixmeasurebuddy.com/api/ system_id / recipes.json
    recipes = []
    for book in dbmodels.Recipe.objects:
        recipes.append(book.tojson())
    return make_response(jsonify(recipes), 200)


@generator.response(status_code=200, schema={'id': 10, 'name': 'test_object'})
@blueprint.route('/api/mmb/<string:mmb_device_id>/recipes', methods=['GET'])
def mmbd_recipes(mmb_device_id: str):  # mixmeasurebuddy.com/api/ system_id / recipes.json
    mmb_device_id = bleach.clean(mmb_device_id)
    # CHECK DEVICE REGISTRATION
    users = dbmodels.Users.objects(linked_device_id=mmb_device_id)
    if len(dbmodels.Users.objects(linked_device_id=mmb_device_id)) <= 0:
        return make_response(jsonify({"err": "please register device"}), 401)

    user = users[0]
    linked_recipes = user.linked_recipes

    ret = []
    for r in linked_recipes:
        ret.append(r.filename)

    return make_response(jsonify(ret), 200)




# @generator.response(status_code=200, schema={'err': None})
@blueprint.route('/api/mmb/<string:mmb_device_id>/link_recipe/<string:recipe_id>/<string:link_state>', methods=['GET'])
def mmbd_link_recipe(mmb_device_id: str, recipe_id: str, link_state: str):
    mmb_device_id = bleach.clean(mmb_device_id)
    recipe_id = bleach.clean(recipe_id)
    link_state = bleach.clean(link_state)
    try:
        if link_state.lower() == "true":
            link_state = True
        elif link_state.lower() == "false":
            link_state = False
        else:
            link_state = bool(int(link_state))
    except:
        return make_response(jsonify({'err': 'link_state parameter invalid 0 or 1'}), 502)

    # CHECK USER EXISTS
    users = dbmodels.Users.objects(linked_device_id=mmb_device_id)
    if len(users) <= 0:
        return make_response(jsonify({"err": "please register device"}), 401)

    # CHECK RECIPE EXISTS
    recipe = dbmodels.Recipe.objects(id=recipe_id)
    if len(recipe) <= 0:
        return make_response(jsonify({"err": "invalid recipe id"}), 401)

    # LINK TOGETHER USER AND RECIPE
    r = recipe.first()
    u = users.first()
    # REMOVE RECIPE IF SELECTED
    if r in u.linked_recipes and not link_state:
        u.linked_recipes.remove(r)
        u.save()
    # ADD RECIPE IF SELECTED
    elif r not in u.linked_recipes and link_state:
        u.linked_recipes.append(r)
        u.save()


    return make_response(jsonify({}), 200)


@generator.response(status_code=200, schema={
    'recipe': {'name': 'Tequila_Sunrise', 'description': 'recipe text', 'version': '1.0.0',
               'ingredients': {'0': 'name'}, 'steps': [{'action': 'scale', 'ingredient': '0', 'amount': 720},
                                                       {'action': 'confirm', 'text': 'press ok'}]},
    'name': 'Recipe_Name'})
@blueprint.route('/api/mmb/<string:mmb_device_id>/recipe/<string:recipe_id>', methods=['GET'])
def mmbd_recipe(mmb_device_id: str, recipe_id: str):
    mmb_device_id = bleach.clean(mmb_device_id)
    recipe_id = bleach.clean(recipe_id)
    # CHECK DEVICE REGISTRATION
    users = dbmodels.Users.objects(linked_device_id=mmb_device_id)
    if len(users) <= 0:
        return make_response(jsonify({"err": "please register device"}), 401)

    user_recipes = dbmodels.Users.objects.get(linked_device_id=mmb_device_id).linked_recipes
    global_recipes = dbmodels.Recipe.objects(filename=recipe_id)
    if len(global_recipes) <= 0:
        return make_response(jsonify({}), 404)

    recipe = global_recipes[0]

    found = False
    for ur in user_recipes:
        if recipe.filename in ur.filename:
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
    ret['filename'] = recipe.filename + ".recipe"
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
    return redirect('/index.html')


app.register_blueprint(blueprint)
generator.generate_swagger(app, destination_path=SWAGGERFILE_PATH)


def prepeare_database():
    # PREPARE DATABASE
    # WE ARE USING PYMONGO TO CHECK THE DATABASE
    pm_db: pymongo.MongoClient = pymongo.MongoClient(DATABASE_CONNECTION_STRING)
    # CREATE DATABASE
    dblist = pm_db.list_database_names()

    if DB_NAME in dblist:
        logging.debug("The MMB_DATABASE {} exists.".format(DB_NAME))
    mmb_database = pm_db[DB_NAME]
    # CREATE COLLECTIONS
    target_collections = [DB_COLLECTION_RECIPES, DB_COLLECTION_USERS, DB_COLLECTION_INGREDIENTS,
                          DB_COLLECTION_CATEGORIES]
    existing_collections = mmb_database.list_collection_names()
    for collection in target_collections:
        if collection in existing_collections:
            logging.debug("The collection {} exists.".format(collection))
        else:
            mmb_database.create_collection(collection)
    # FINALLY CLOSE CONNECTION
    pm_db.close()


if __name__ == "__main__":
    # CHECK DB CONNECTION

    # CREATE mongoengine CONNECTION so we can use mongoengine later on
    cs = "{}/{}".format(DATABASE_CONNECTION_STRING, DATABASE_NAME)
    logging.debug(cs)
    mongoengine.register_connection(alias=DEFAULT_CONNECTION_NAME)
    mongoengine.connect(DATABASE_NAME, host=cs)

    # CREATE ADMIN USER
    if len(dbmodels.Users.objects(linked_device_id="1337")) <= 0:
        user = dbmodels.Users(name="MixMeasureBuddy Owner A")
        user.linked_device_id = "1337"
        user.permissions = 1
        user.save()
    if len(dbmodels.Users.objects(linked_device_id="1338")) <= 0:
        user = dbmodels.Users(name="MixMeasureBuddy Owner B")
        user.linked_device_id = "1338"
        user.permissions = 1
        user.save()

    # CREATE CATEGORY
    categories = ["Cocktails", "Virgin-Cocktails", "Longdrinks"]
    for c in categories:
        if len(dbmodels.Category.objects(name=c)) <= 0:
            dbmodels.Category(name=c).save()

    # CREATE  INGREDIENTS
    test_ing = ["Aperol", "Prosecco", "Elderflower-Syrup", "Sodawater", "Pineapple-Juice", "", "Cream", "white Rum",
                "Strawberry-Syrup", "Malibu-Coconut", "Crushed Ice", "Coconut-Juice", "Strawberries", "white Tequila",
                "Grenadine", "Orange-Juice"]

    for i in test_ing:
        if len(dbmodels.Ingredient.objects(name=i)) <= 0:
            r = dbmodels.Ingredient(name=i).save()

    # CREATE TEST RECIPES
    if len(dbmodels.Recipe.objects(name="Hugo")) <= 0:
        i_list = []
        i_list.append(dbmodels.Ingredient.objects(name="Prosecco")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Sodawater")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Elderflower-Syrup")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Crushed Ice")[0])

        i_steps = []
        i_steps.append(
            dbmodels.Step(amount=150, action="scale", ingredient=dbmodels.Ingredient.objects(name="Prosecco")[0]))
        i_steps.append(
            dbmodels.Step(amount=100, action="scale", ingredient=dbmodels.Ingredient.objects(name="Sodawater")[0]))
        i_steps.append(dbmodels.Step(amount=30, action="scale",
                                     ingredient=dbmodels.Ingredient.objects(name="Elderflower-Syrup")[0]))

        ra = dbmodels.Recipe()
        ra.name = "Hugo"
        ra.filename = urllib.parse.quote(ra.name.replace(' ', '_'))
        ra.category = dbmodels.Category.objects(name="Longdrinks")
        ra.description = "Hugo is a low-alcohol cocktail made with prosecco, lemon balm or elderflower syrup, fresh mint and mineral or soda water;"
        ra.ingredients = i_list
        ra.default_recipe = True
        ra.author = dbmodels.Users.objects(linked_device_id="1337")[0]
        ra.steps = i_steps
        ra.save()

    if len(dbmodels.Recipe.objects(name="Aperol Spritz")) <= 0:
        i_list = []
        i_list.append(dbmodels.Ingredient.objects(name="Aperol")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Prosecco")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Sodawater")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Crushed Ice")[0])

        i_steps = []
        i_steps.append(
            dbmodels.Step(amount=60, action="scale", ingredient=dbmodels.Ingredient.objects(name="Aperol")[0]))
        i_steps.append(
            dbmodels.Step(amount=80, action="scale", ingredient=dbmodels.Ingredient.objects(name="Prosecco")[0]))
        i_steps.append(
            dbmodels.Step(amount=10, action="scale", ingredient=dbmodels.Ingredient.objects(name="Sodawater")[0]))

        ra = dbmodels.Recipe()
        ra.name = "Aperol Spritz"
        ra.filename = urllib.parse.quote(ra.name.replace(' ', '_'))
        ra.category = dbmodels.Category.objects(name="Longdrinks")
        ra.description = "The Spritz, also Sprizz or Veneziano, is a mixed drink made from Prosecco or white wine and mineral water and a liqueur."
        ra.ingredients = i_list
        ra.default_recipe = True
        ra.author = dbmodels.Users.objects(linked_device_id="1337")[0]
        ra.steps = i_steps
        ra.save()

    if len(dbmodels.Recipe.objects(name="Tequila Sunrise")) <= 0:
        i_list = []
        i_list.append(dbmodels.Ingredient.objects(name="white Tequila")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Orange-Juice")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Grenadine")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Crushed Ice")[0])

        i_steps = []
        i_steps.append(
            dbmodels.Step(amount=20, action="scale", ingredient=dbmodels.Ingredient.objects(name="white Tequila")[0]))
        i_steps.append(
            dbmodels.Step(amount=40, action="scale", ingredient=dbmodels.Ingredient.objects(name="Grenadine")[0]))
        i_steps.append(
            dbmodels.Step(amount=110, action="scale", ingredient=dbmodels.Ingredient.objects(name="Orange-Juice")[0]))
        i_steps.append(dbmodels.Step(action="wait", text="MIX", amount=30))
        i_steps.append(dbmodels.Step(action="confirm", text="ADD ICE"))

        ra = dbmodels.Recipe()
        ra.name = "Tequila Sunrise"
        ra.filename = urllib.parse.quote(ra.name.replace(' ', '_'))
        ra.category = dbmodels.Category.objects(name="Cocktails")
        ra.description = "A nice Tequila Sunrise Cocktail"
        ra.ingredients = i_list
        ra.default_recipe = True
        ra.author = dbmodels.Users.objects(linked_device_id="1337")[0]
        ra.steps = i_steps
        ra.save()

    if len(dbmodels.Recipe.objects(name="Strawberry Colada Lotte")) <= 0:
        i_list = []
        i_list.append(dbmodels.Ingredient.objects(name="Malibu-Coconut")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Strawberry-Syrup")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Pineapple-Juice")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Cream")[0])

        i_steps = []
        i_steps.append(
            dbmodels.Step(amount=50, action="scale", ingredient=dbmodels.Ingredient.objects(name="Malibu-Coconut")[0]))
        i_steps.append(dbmodels.Step(amount=30, action="scale",
                                     ingredient=dbmodels.Ingredient.objects(name="Strawberry-Syrup")[0]))
        i_steps.append(
            dbmodels.Step(amount=20, action="scale", ingredient=dbmodels.Ingredient.objects(name="Cream")[0]))
        i_steps.append(
            dbmodels.Step(amount=80, action="scale", ingredient=dbmodels.Ingredient.objects(name="Pineapple-Juice")[0]))

        rb = dbmodels.Recipe()
        rb.name = "Strawberry Colada Lotte"
        rb.filename = urllib.parse.quote(rb.name.replace(' ', '_'))
        rb.category = dbmodels.Category.objects(name="Cocktails")
        rb.description = "Lottes delicious cocktail with strawberries"
        rb.ingredients = i_list
        rb.default_recipe = True
        rb.author = dbmodels.Users.objects(linked_device_id="1338")[0]
        rb.steps = i_steps
        rb.save()

    if len(dbmodels.Recipe.objects(name="Pina Colada")) <= 0:
        i_list = []
        i_list.append(dbmodels.Ingredient.objects(name="Malibu-Coconut")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Strawberry-Syrup")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Pineapple-Juice")[0])
        i_list.append(dbmodels.Ingredient.objects(name="Cream")[0])

        i_steps = []
        i_steps.append(
            dbmodels.Step(amount=40, action="scale", ingredient=dbmodels.Ingredient.objects(name="Malibu-Coconut")[0]))
        i_steps.append(
            dbmodels.Step(amount=20, action="scale", ingredient=dbmodels.Ingredient.objects(name="Cream")[0]))
        i_steps.append(
            dbmodels.Step(amount=80, action="scale", ingredient=dbmodels.Ingredient.objects(name="Pineapple-Juice")[0]))

        rb = dbmodels.Recipe()
        rb.name = "Pina Colada"
        rb.filename = urllib.parse.quote(rb.name.replace(' ', '_'))
        rb.category = dbmodels.Category.objects(name="Cocktails")
        rb.description = "One of the most popular tropical cocktails from the Caribbean is the Pina Colada, simply delicious with strawberries"
        rb.ingredients = i_list
        rb.default_recipe = True
        rb.author = dbmodels.Users.objects(linked_device_id="1338")[0]
        rb.steps = i_steps
        rb.save()

    # START FLASK
    app.run(host=os.environ.get("API_SERVER_BIND_ADDR", '0.0.0.0'), port=os.environ.get("API_SERVER_PORT", 5500),
            debug=True)

from flask import Flask, jsonify, make_response, Blueprint, redirect
from dotenv import load_dotenv
import os
from pathlib import Path
from flask_swagger_generator.components import SwaggerVersion
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger_generator.generators import Generator
from flask_swagger_generator.utils import SecurityType
import logging
from configparser import ConfigParser
# IMPORT CUSTOM DATABASE MODELS
import dbmodels

logging.getLogger().setLevel(logging.DEBUG)
load_dotenv() # LOAD .env

config = ConfigParser()
config.read(Path.joinpath(Path(__file__).parent, Path("config.cfg")))

SWAGGER_URL = '/docs'  # URL for exposing Swagger UI (without trailing '/')
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





# SPECIFI GENERATED FOR DEVICES
# ["resipe_file_uri_relative"]
@generator.response(status_code=200, schema={'id': 10, 'name': 'test_object'})
@blueprint.route('/mmb/<string:mmb_device_id>', methods=['GET'])
def mmbd_recipes(mmb_device_id: str):  # mixmeasurebuddy.com/api/ system_id / recipes.json
    data: list = [
        "Tequila_Sunrise",
    ]
    return make_response(jsonify(data), 200)

@generator.response(status_code=200, schema={'recipe': {'name': 'Tequila_Sunrise', 'description': 'recipe text','version': '1.0.0','ingredients': {'0': 'name'},'steps':[{'action':'scale', 'ingredient':'0', 'amount':720},{'action':'confirm', 'text':'press ok'}]}, 'name': 'Recipe_Name'})
@blueprint.route('/mmb/<string:mmb_device_id>/<string:recipe_id>', methods=['GET'])
def mmbd_recipe(mmb_device_id: str, recipe_id: str):
    data: dict = {


    }
    return make_response(jsonify(data), 200)





@blueprint.route('/')
def index():
    return redirect(SWAGGER_URL)



app.register_blueprint(blueprint)
generator.generate_swagger(app, destination_path=SWAGGERFILE_PATH)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("API_SERVER_PORT", 9090), debug=True)

from flask import Flask, jsonify, make_response
from dotenv import load_dotenv
import os
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger_generator.generators import Generator
from flask_swagger_generator.specifiers import SwaggerVersion
from flask_swagger_generator.utils import SecurityType

load_dotenv() # LOAD .env

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://petstore.swagger.io/v2/swagger.json'  # Our API url (can of course be a local resource)


app = Flask(__name__)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)




# SPECIFI GENERATED FOR DEVICES
# ["resipe_file_uri_relative"]
@app.route('/mmb/<mmb_device_id>/recipes', methods=['GET', 'POST']) # mixmeasurebuddy.com/api/ system_id / recipes.json
def mmbd_recipes(mmb_device_id: str):  # put application's code here
    data: list = [
        "Tequila_Sunrise",
    ]
    return make_response(jsonify(data), 200)

@app.route('/mmb/<mmb_device_id>/<recipe_id>', methods=['GET', 'POST'])
def mmbd_recipe(mmb_device_id:str, recipe_id: str):
    data: dict = {
        "name": "Tequila_Sunrise",
        "recipe": {}
    }
    return make_response(jsonify(data), 200)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("API_SERVER_PORT", 9090), debug=True)

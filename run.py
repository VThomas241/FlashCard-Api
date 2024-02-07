from flask import Flask
from flask_cors import CORS
from app import api

#* Must be imported before the rest of the imports to load the dotenv file first (required for pytest)
from app.core.config import Development
 
from app.core.utils.swagger import SwaggerModel
from app.namespaces import ns_list


# def create_app():
app = Flask(__name__)
CORS(app,origins=['http://localhost:5173'])
app.config.from_object(Development)
app.app_context().push()
api.init_app(app)
    # return app

# app = create_app()

for ns in ns_list: api.add_namespace(ns)
for model in SwaggerModel.models: api.models[model.name] = model

if __name__ == '__main__':
    app.run()

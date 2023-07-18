from flask import Flask
from app import api
from app.namespaces import ns_list
from app.core.utils.swagger import model_list
from app.core.config import Development


app = Flask(__name__)
app.config.from_object(Development)
app.app_context().push()
api.init_app(app)

for ns in ns_list: api.add_namespace(ns)
for model in model_list: api.models[model.name] = model

if __name__ == '__main__':
    app.run()

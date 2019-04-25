from flask import Flask
from apis import api
import json
app = Flask(__name__)
app.config['SERVER_NAME'] = "localhost:5000"
api.init_app(app)
with app.app_context():
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    print(json.dumps(data))

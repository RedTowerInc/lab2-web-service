from flask import Flask
from flasgger import Swagger
from sitepart.sitepart import sitepart

app = Flask(__name__)
swagger = Swagger(app)

# Подключение части API
app.register_blueprint(sitepart, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)

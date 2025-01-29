from flask import Flask, render_template
from flasgger import Swagger
from sitepart.sitepart import sitepart

app = Flask(__name__)
swagger = Swagger(app)

# Подключаем API
app.register_blueprint(sitepart, url_prefix="/api")


@app.route('/')
def index():
    """Главная страница с таблицей комплектующих"""
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

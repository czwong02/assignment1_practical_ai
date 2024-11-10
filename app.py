from flask import Flask, request, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint
from analyze import read_image

app = Flask(__name__, template_folder='templates')

SWAGGER_URL = '/apidocs'  # URL for exposing Swagger UI
API_URL = '/static/swagger.yml'  # URL for the Swagger YAML file

# Create Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Computer Vision Azure API"
    }
)

# Register Swagger UI blueprint at /apidocs
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/static/swagger.yml")  # Changed route to match API_URL
def swagger_yaml():
    return app.send_static_file('swagger.yml')

@app.route("/api/v1/analysis/", methods=['POST'])
def analysis():
    try:
        get_json = request.get_json()
        image_uri = get_json['uri']
    except:
        return jsonify({'error': 'Missing URI in JSON'}), 400

    try:
        res = read_image(image_uri)
        response_data = {
            "text": res
        }
        return jsonify(response_data), 200
    except:
        return jsonify({'error': 'Error in processing'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
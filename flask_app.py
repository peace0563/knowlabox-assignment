from flask import Flask, request, jsonify, send_file,  make_response, redirect
from flask_cors import CORS, cross_origin
from basic_func import get_image_by_id, conv_image_func

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "12345678"


@app.after_request
def after_request(response):
    response.headers.set("Access-Control-Allow-Credentials", "true")
    return response


@app.route('/convertimage', methods=['POST'])
def convertimage():
    output_json = {}
    form_data = request.get_json(force=True)
    data = conv_image_func(form_data)

    output_json = {
        "status":   data['status'],
        "response": data['response'],
        "message":  data['message']
    }
    return jsonify(output_json)


@app.route('/getimagebyfileid', methods=['POST'])
def getimagebyfileid():
    output_json = {}
    form_data = request.get_json(force=True)
    data = get_image_by_id(form_data)

    output_json = {
        "status":   data['status'],
        "response": data['response'],
        "message":  data['message']
    }
    return jsonify(output_json)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)

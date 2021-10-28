from flask import Flask, json, request, jsonify
from flask_restful import Api, Resource
app = Flask (__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'

@app.route('/user/<userName>')
def hello_user(userName):
    return 'Hello, %s!'%(userName)

@app.route('/userLogin', methods = ['POST'])
def userLogin():
    user = request.get_json()
    return jsonify(user)

@app.route('/environment/<langauge>')
def environment(langauge):
    return jsonify({"language":langauge})


if __name__ == "__main__":
    app.run()

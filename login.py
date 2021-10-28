from flask import Flask, request
from flask_restful import Api, Resource
from flask_restful import reqparse
import re

app = Flask(__name__)
api = Api(app)

id_list = ["qlalf9824@naver.com", "gayoung5401@gmail.com", "asdfeg@viewmagine.com"]
id = "qlalf9824@viewmagine.com"
pw = "1q2w3e"
pattern = "(^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class Login(Resource):
	def get(self):
            try:
                param_dict = request.args.to_dict()

                reid = param_dict['id']

                if(reid in id_list):
                    return {
                        'Response' : {
                            'message' : 'This is a duplicate ID.'
                        }
                    }
                else:
                    return {
                        'Response' : {
                            'message' : 'This is the ID that you can use.'
                        }
                    }
            except Exception as e:
                return {
                    'Response' : {
                        'Message' : 'Error in Processing',
                        'Result': 'Error',
                        'Details': str(e)
                    }
                }

	def post(self):
            try:
                params = request.get_json(force=True)

                reid = params['id']
                repw = params['pw']
                
                pattern = "^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

                if re.match(pattern, reid)== None:
                    return {
                        'Response' : {
                            'message' : 'Wrong email'
                        }
                    }
                elif(reid == id and repw == pw):
                    return {
                        'Response' : {
                            'message' : 'Login!'
                        }
                    }
                else:
                    return {
                        'Response' : {
                            'message' : 'Wrong ID or Password'
                        }
                    }
            except Exception as e:
                return {
                    'Response' : {
                        'Message' : 'Error in Processing',
                        'Result': 'Error',
                        'Details': str(e)
                    }
                }

api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)
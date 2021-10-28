from flask import Flask, request, render_template
from flask.templating import render_template_string
from flask_restful import Api, Resource
from flask_restful import reqparse

# isfile()
import os.path


app = Flask(__name__)
api = Api(app)

reder_image_file = ""

@app.route('/')
def printResult():
    # return "Result"
    # print(reder_image_file)
    # return render_template('home.html', image_file = reder_image_file)
    return render_template('home.html', image_file = reder_image_file, value1 = 0, value2 = 0)



class ImageProcess(Resource):
    def get(self):
        return "GET"

    def post(self):
        try:
            params = request.get_json(force=True)

            img_path = params['img_path']
            img_name = params['img_name']

            result_img_path = "result_img/"
            result_img_name = "result_" + img_name

            global reder_image_file
            reder_image_file = "images/" + result_img_name

            print(reder_image_file)

            whole_parking_slot_num = 0
            empty_parking_slot_num = 0

            # temp = "images/" + result_img_name

            # print(temp)
            # print(reder_image_file)


            if os.path.isfile(img_path + img_name):
                #image processing
                print("###########Image Processing....############")
                
                return{
                    "Response" : {
                        "Message": "Success",
                        "Image Path": result_img_path,
                        "Image Name": result_img_name,
                        "Whole Parking slot": whole_parking_slot_num,
                        "Empty Parking slot": empty_parking_slot_num
                    }
                }
            else:
                return{
                    "Response" : {
                        "Message": "No file in Directory"
                    }
                }
        except Exception as e:
            return {
                "Response" : {
                    "Message": "Error in Processing",
                    "Details": str(e)
                }
            }


api.add_resource(ImageProcess, '/process')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


            

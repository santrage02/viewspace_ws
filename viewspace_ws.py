from flask import Flask, request, render_template
from flask.templating import render_template_string
from flask_restful import Api, Resource
from flask_restful import reqparse
from werkzeug.utils import secure_filename
from yolov5 import *

# isfile()
import os.path

import sys
sys.path.append('yolov5')

from yolov5.test import main
import yolov5


trial = 0

app = Flask(__name__)
api = Api(app)

render_img_name = ""
whole_parking_slot_num = 0
empty_parking_slot_num = 0

@app.route('/')
def printResult():
    # return "Result"
    # print(render_img_name)
    # return render_template('home.html', image_file = render_img_name)
    return render_template('home.html', image_file = render_img_name, value1 = whole_parking_slot_num, value2 = empty_parking_slot_num)


@app.route('/fileupload', methods=['POST'])
def file_upload():
    try:
        file = request.files['file'] 
        
        filename = secure_filename(file.filename)

        file.save(os.path.join("video/", filename))

        return {
            "Response": {
                "Message": "Success",
                "Image_path": "video/",
                "Image_name": filename
            }
        }
    except Exception as e:
        return {
            "Response" : {
                "Message": "Error"
            }
        }


class ImageProcess(Resource):
    def get(self):
        return "GET"

    def post(self):
        try:
            params = request.get_json(force=True)


            img_path = params['img_path'] #nano에서 보낸 영상 디렉토리
            img_name = params['img_name'] #nano에서 보낸 영상 이름

            # result_img_path = "result_img/" # 영상 처리 후 저장될 디렉토리
            # result_img_name = "result_" + img_name # 영상 처리 후 저장 이름

            result_img_path = "static/images"
            result_img_name = "result_" + img_name

            # html
            global render_img_name
            # render_img_name = "images/" + result_img_name
            # render_img_name = "images/" + img_name
            # render_img_name = result_img_name
            render_img_name = "images/" + result_img_name
            print(render_img_name)

            global whole_parking_slot_num
            global empty_parking_slot_num

            # temp = "images/" + result_img_name

            # print(temp)
            # print(render_img_name)


            if os.path.isfile(img_path + img_name):
                #video processing

                print("###########Image Processing....############")
                
                # 결과 이미지 저장 위치: static/images
                # command = 'python3 yolov5/detect.py --source ' + img_path + img_name + ' --weights yolov5/car_detection.pt --conf 0.6 --project=static --name=images --exist-ok --line-thickness 1'
                command = 'python3 yolov5/detect.py --source ' + img_path + img_name + ' --weights yolov5/car_detection.pt --conf 0.6 --project=result_img --name=images --exist-ok --line-thickness 1'
                os.system(command)

                # Find Empty Slot Box, Find whole / empty parking slot number
                whole_parking_slot_num, empty_parking_slot_num = main(img_name)
                
                # print("---------------------------------------" + result)

                # print(whole_parking_slot_num)
                # print(empty_parking_slot_num)

                # print("-----------------" + result)

                # os.system('cd /home/jingeonshin/viewspace_model_practice/yolov5;python3 detect.py --source /home/jingeonshin/viewspace_model_practice/yolov5/data/images/20161225_TPZ_00094.png --weights /home/jingeonshin/viewspace_model_practice/yolov5/car_detection.pt --conf 0.6 --project=/home/jingeonshin/viewspace_model_practice/result --name=test --exist-ok --line-thickness 1')
                # os.system('python3 yolov5/detect.py --source img/p_test1.png --weights yolov5/car_detection.pt --conf 0.6 --project=result_img --name=test --exist-ok --line-thickness 1')


                
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


            

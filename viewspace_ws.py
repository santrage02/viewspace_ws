from flask import Flask, request, render_template
from flask.templating import render_template_string
from flask_restful import Api, Resource
from flask_restful import reqparse

# isfile()
import os.path

trial = 0

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


            img_path = params['img_path'] #nano에서 보낸 영상 디렉토리
            img_name = params['img_name'] #nano에서 보낸 영상 이름

            # result_img_path = "result_img/" # 영상 처리 후 저장될 디렉토리
            # result_img_name = "result_" + img_name # 영상 처리 후 저장 이름

            result_img_path = "static/images"
            result_img_name = img_name

            # html
            global reder_image_file
            # reder_image_file = "images/" + result_img_name
            reder_image_file = "images/" + img_name
            # print(reder_image_file)

            whole_parking_slot_num = 0
            empty_parking_slot_num = 0

            # temp = "images/" + result_img_name

            # print(temp)
            # print(reder_image_file)


            if os.path.isfile(img_path + img_name):
                #video processing

                print("###########Image Processing....############")
                
                # 결과 이미지 저장 위치: static/images
                command = 'python3 yolov5/detect.py --source ' + img_path + img_name + ' --weights yolov5/car_detection.pt --conf 0.6 --project=static --name=images --exist-ok --line-thickness 1'
                os.system(command)
                
                # 결과 텍스트파일 읽기 추가 필요(전차 자리수, 빈 자리수, 디렉토리 이름, 결과 이미지 이름)
                # 현재 결과 디렉토리 -> static/images , 결과 이미지 이름: input 이미지 그대로




                # os.system('ls -al')
                # os.system('cd /home/jingeonshin/viewspace_model_practice/yolov5')
                # os.system('ls -al')
                # os.system('cd /home/jingeonshin/viewspace_model_practice/yolov5;python3 detect.py --source /home/jingeonshin/viewspace_model_practice/yolov5/data/images/20161225_TPZ_00094.png --weights /home/jingeonshin/viewspace_model_practice/yolov5/car_detection.pt --conf 0.6 --project=/home/jingeonshin/viewspace_model_practice/result --name=test --exist-ok --line-thickness 1')
                # os.system('python3 yolov5/detect.py --source img/p_test1.png --weights yolov5/car_detection.pt --conf 0.6 --project=result_img --name=test --exist-ok --line-thickness 1')

                # stream = os.popen('ls -l')
                # output = stream.read()
                # print("____________________")
                # print(output)

                
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


            

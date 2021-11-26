from util import *
from getIoU import *
import os.path

def main(img_name):
  # transform parking slot from yolo format to (x1,y1,x2,y2)
  # img_w = 1280
  # img_h = 720
  img_w = 2500
  img_h = 2500
  path1 = os.getcwd() + "/data/stitched_parkingspace.txt"
  # path1 = os.getcwd() + "/data/parkingspace.txt"
  parking_lots = yolo_to_org(path1, img_w, img_h)
  print(parking_lots)

  # input_path = "../data/car_info.txt"
  input_path = os.getcwd() + "/data/car_info.txt"
  # get file with yolo format 
  fl = open(input_path, 'r')
  data = fl.readlines()
  fl.close()

  cars = []
  for temp in data:
    x1, y1, x2, y2 = map(float, temp.split(',')) # the first value is not used(class id)
    tmp = [x1, y1, x2, y2]
    cars.append(tmp)

  print("Group Example >> sort_and_group_parkinglot(parking_lots, epsilon = 20) ->")
  x_grouped_lots, y_grouped_lots = sort_and_group_parkinglot(parking_lots, epsilon = 20)
  grouped_lots = {
      "x_grouped_lots": x_grouped_lots,
      "y_grouped_lots": y_grouped_lots
  }
  pprint(grouped_lots)
  pprint(cars)

  # print("Find car park location Example >> find_car_park_location() ->")
  # lot, iou = find_car_park_location(carex, grouped_lots, epsilon = 20, threshold = 0.4)
  # print(lot, iou)

  empty_grouped_lots = classify_empty_parking_lots(cars, grouped_lots, epsilon = 20, threshold = 0.4)
  print("Empty Grouped Lots")
  pprint(empty_grouped_lots)

  print("Get iou example")
  print("get_iou([10, 10, 20, 20], [15, 15, 25, 25], epsilon=1e-5) -> ", get_iou([10, 10, 20, 20], [15, 15, 25, 25], epsilon=1e-5))

  empty_lots = []
  for group in empty_grouped_lots["x_grouped_lots"]:
    if group == None:
      continue;    
    
    for lot in group:
      empty_lots.append(lot)
  for group in empty_grouped_lots["y_grouped_lots"]:
    for lot in group:
      empty_lots.append(lot)
  print("Empty lots")
  pprint(empty_lots)

  print("OKAY")

  total_lots_n = len(parking_lots)
  empty_lots_n = len(empty_lots)
  

  # return total_lots_n, empty_lots_n
  # visualize empty slot


            
  # draw_rect(empty_lots,\
  #           os.getcwd() + "/img/parkingspace.png", \
  #           os.getcwd() + "/static/images/result_parkingspace.png",total_lots_n,empty_lots_n)

  draw_rect(empty_lots,\
            os.getcwd() + "/img/" + img_name, \
            os.getcwd() + "/static/images/" + "result_" + img_name,total_lots_n,empty_lots_n)

  return total_lots_n, empty_lots_n


if __name__ == '__main__':
  # total, empty = main(img_name)
  total, empty = main("stitched_parkingspace.png")
  # return total, empty
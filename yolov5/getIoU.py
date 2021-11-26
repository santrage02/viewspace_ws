from functools import cmp_to_key
from pprint import pprint

def classify_with_direction(lots):
  x_lots = []
  y_lots = []
  for lot in lots:
    if ((lot[2] - lot[0]) > (lot[3] - lot[1])):
      x_lots.append(lot)
    else:
      y_lots.append(lot)
  return x_lots, y_lots
  
def compare(a, b, epsilon = 20): # a, b: [x1, y1, x2, y2]
  if (abs(a[0] - b[0]) > epsilon): # 같은 라인이 아니면 (epsilon은 오차범위)
    if (a[0] > b[0]):
      return 1
    else:
      return -1
  else:
    if(a[1] > b[1]):
      return 1
    else:
      return -1
    
def group_lot(lots, direction, epsilon):
  lots_grouped = []
  min = -1
  group = None
  drt = 0 if direction == 'x' else 1
  for lot in lots: 
    if lot[drt] > min:
      if group != None:
        lots_grouped.append(group) 
      min = lot[drt] + epsilon
      group = []
      group.append(lot)
    else:
      group.append(lot)
  lots_grouped.append(group)

  return lots_grouped

    
'''
lot: list of parking lots, list[[x1,y1,x2,y2], ...]
line_axis: axis of line alignment of parking lot, "x" or "y"
''' 
def sort_and_group_parkinglot(lots, epsilon) -> tuple: # (x_grouped_lot, y_grouped_lot)
  x_lots, y_lots = classify_with_direction(lots) #x_lots: ㅁ y_lots: E ()
  x_s = sorted(x_lots, key = cmp_to_key(lambda x,y: compare(x, y, epsilon=epsilon))) 
  y_s = sorted(y_lots, key = cmp_to_key(lambda x,y: compare(x, y, epsilon=epsilon)))
  return group_lot(x_s, 'x', 20), group_lot(y_s, 'y', 20)

'''
  a: x1, y1, x2, y2, c1, c2 (center point) 
  b: x1, y1, x2, y2
  epsilon: prevent division by zero
'''
def get_iou(a, b, epsilon=1e-5):
  x1 = max(a[0], b[0])
  y1 = max(a[1], b[1])
  x2 = min(a[2], b[2])
  y2 = min(a[3], b[3])

  # AREA OF OVERLAP - Area where the boxes intersect
  width = (x2 - x1)
  height = (y2 - y1)
  # handle case where there is NO overlap
  if (width<0) or (height <0):
      return 0.0
  area_overlap = width * height

  # COMBINED AREA
  area_a = (a[2] - a[0]) * (a[3] - a[1])
  area_b = (b[2] - b[0]) * (b[3] - b[1])
  area_combined = area_a + area_b - area_overlap

  # RATIO OF AREA OF OVERLAP OVER COMBINED AREA
  iou = area_overlap / (area_combined+epsilon)
  return iou

def car_park_direction(car):
  return 'x' if ((car[2] - car[0]) > (car[3] - car[1])) else 'y'

def find_car_park_location(car, grouped_lots, epsilon, threshold): 
  '''  
    car: [x1, y1, x2, y2] Ex) [325, 67, 411, 100]
    grouped_lots: [[[x1, y1, x2, y2],...,[]],[[],...,[]],...,[]]
    lineaxis: 'x' / 'y'
  '''
  
  (axis, a, b) = ("x_grouped_lots", 0, 1) if (car_park_direction(car) == 'x') else ("y_grouped_lots", 1, 0)
  
  for group in grouped_lots[axis]:
    if (group[a][a] - epsilon > car[a+2] or group[a][a+2] + epsilon < car[a]):
      continue
    else:
      for lot in group:
        if ((lot[b] - epsilon) > car[b+2] or (lot[b+2] + epsilon) < car[b]):
          continue
        iou = get_iou(car, lot)
        if (iou > threshold):
          return lot, iou
        else:
          print('continue')
  return False, False

def remove_car_park_location(car, grouped_lots, epsilon, threshold): 
  '''  
    car: [x1, y1, x2, y2] Ex) [325, 67, 411, 100]
    grouped_lots: [[[x1, y1, x2, y2],...,[]],[[],...,[]],...,[]]
    lineaxis: 'x' / 'y'
  '''
  
  (axis, a, b) = ("x_grouped_lots", 0, 1) if (car_park_direction(car) == 'x') else ("y_grouped_lots", 1, 0)
  
  for group in grouped_lots[axis]:
    if (group[a][a] - epsilon > car[a+2] or group[a][a+2] + epsilon < car[a]):
      continue
    else:
      for lot in group:
        if ((lot[b] - epsilon) > car[b+2] or (lot[b+2] + epsilon) < car[b]):
          continue
        print("get iou of ", car, lot)
        iou = get_iou(car, lot)
        if (iou > threshold):
          print("remove", lot)
          # del lot
          group.remove(lot)

          return grouped_lots
        else:
          print(iou, 'continue')
  return grouped_lots

def classify_empty_parking_lots(cars, grouped_lots, epsilon, threshold):
  for car in cars:
    (axis, a, b) = ("x_grouped_lots", 0, 1) if (car_park_direction(car) == 'x') else ("y_grouped_lots", 1, 0)
    print("finding", car)
    if grouped_lots[axis] == [None]:
          continue

    for group in grouped_lots[axis]:
      if (not len(group) or group[a][a] - epsilon > car[a+2] or group[a][a+2] + epsilon < car[a]):
        continue
      else:
        for lot in group:
          if ((lot[b] - epsilon) > car[b+2] or (lot[b+2] + epsilon) < car[b]):
            continue
          iou = get_iou(car, lot)
          if (iou > threshold):
            print("remove", lot, iou)
            # del lot
            group.remove(lot)
          else:
            print(iou, 'continue')
  return grouped_lots

if(__name__ == "__main__"): 
  carex = [857.0, 403.0, 896.0, 483.0, 0.9015883803367615, 1.0]
  cars = [[760.0, 537.0, 805.0, 623.0, 0.8996853828430176, 1.0], [906.0, 168.0, 977.0, 202.0, 0.8953076601028442, 1.0], [743.0, 165.0, 813.0, 200.0, 0.8913708329200745, 1.0], [657.0, 253.0, 726.0, 288.0, 0.8903429508209229, 1.0], [903.0, 13.0, 972.0, 46.0, 0.8895552754402161, 1.0], [656.0, 333.0, 725.0, 369.0, 0.8882485032081604, 1.0], [382.0, 63.0, 453.0, 100.0, 0.8877540826797485, 1.0], [321.0, 212.0, 367.0, 296.0, 0.8871977925300598, 1.0], [740.0, 125.0, 811.0, 161.0, 0.8869909048080444, 1.0], [471.0, 21.0, 539.0, 51.0, 0.8836174607276917, 1.0], [648.0, 15.0, 720.0, 48.0, 0.8808851838111877, 1.0], [734.0, 48.0, 805.0, 83.0, 0.8787699937820435, 1.0], [654.0, 129.0, 730.0, 164.0, 0.8786641359329224, 1.0], [903.0, 49.0, 975.0, 82.0, 0.8756980299949646, 1.0], [470.0, 174.0, 552.0, 211.0, 0.87498939037323, 1.0], [657.0, 291.0, 733.0, 326.0, 0.8741716742515564, 1.0], [207.0, 505.0, 297.0, 549.0, 0.8741271495819092, 1.0], [745.0, 204.0, 824.0, 242.0, 0.8738001585006714, 1.0], [468.0, 337.0, 551.0, 376.0, 0.873328685760498, 1.0], [213.0, 572.0, 301.0, 643.0, 0.8726636171340942, 1.0], [468.0, 299.0, 552.0, 337.0, 0.8712997436523438, 1.0], [464.0, 54.0, 545.0, 92.0, 0.8709935545921326, 1.0], [383.0, 139.0, 454.0, 175.0, 0.8708500266075134, 1.0], [902.0, 126.0, 980.0, 167.0, 0.8694061040878296, 1.0], [644.0, 168.0, 729.0, 206.0, 0.8689189553260803, 1.0], [377.0, 25.0, 457.0, 61.0, 0.8672209978103638, 1.0], [701.0, 530.0, 749.0, 625.0, 0.8671296834945679, 1.0], [730.0, 11.0, 810.0, 46.0, 0.8671103715896606, 1.0], [376.0, 179.0, 451.0, 215.0, 0.866923451423645, 1.0], [651.0, 210.0, 732.0, 248.0, 0.8647388815879822, 1.0], [378.0, 220.0, 455.0, 255.0, 0.864508867263794, 1.0], [646.0, 89.0, 726.0, 124.0, 0.8641877174377441, 1.0], [393.0, 383.0, 468.0, 421.0, 0.8628448247909546, 1.0], [466.0, 133.0, 551.0, 172.0, 0.8624868988990784, 1.0], [469.0, 96.0, 546.0, 132.0, 0.860515296459198, 1.0], [476.0, 256.0, 557.0, 292.0, 0.8582172393798828, 1.0], [476.0, 385.0, 557.0, 420.0, 0.8569726943969727, 1.0], [387.0, 260.0, 465.0, 296.0, 0.853884220123291, 1.0], [382.0, 341.0, 459.0, 378.0, 0.8535956740379333, 1.0], [733.0, 86.0, 808.0, 121.0, 0.8517389297485352, 1.0], [469.0, 216.0, 554.0, 254.0, 0.849090039730072, 1.0], [644.0, 49.0, 723.0, 86.0, 0.8468790054321289, 1.0], [203.0, 386.0, 279.0, 420.0, 0.8451154232025146, 1.0], [382.0, 301.0, 461.0, 337.0, 0.844620406627655, 1.0], [917.0, 203.0, 987.0, 233.0, 0.8428129553794861, 1.0], [660.0, 375.0, 742.0, 424.0, 0.8408766388893127, 1.0], [379.0, 0.0, 455.0, 23.0, 0.8385058641433716, 1.0], [740.0, 284.0, 812.0, 326.0, 0.8382743000984192, 1.0], [206.0, 33.0, 281.0, 71.0, 0.8360219597816467, 1.0], [354.0, 551.0, 396.0, 634.0, 0.8352422714233398, 1.0], [899.0, 82.0, 978.0, 123.0, 0.8327516913414001, 1.0], [384.0, 101.0, 460.0, 137.0, 0.8298836350440979, 1.0], [640.0, 539.0, 685.0, 617.0, 0.8244346976280212, 1.0], [741.0, 247.0, 822.0, 283.0, 0.8035585880279541, 1.0], [205.0, 446.0, 285.0, 484.0, 0.801486611366272, 1.0], [820.0, 515.0, 857.0, 601.0, 0.7992419600486755, 1.0], [209.0, 92.0, 281.0, 131.0, 0.7982006072998047, 1.0], [207.0, 209.0, 267.0, 240.0, 0.7967999577522278, 1.0], [412.0, 558.0, 456.0, 635.0, 0.7903014421463013, 1.0], [206.0, 2.0, 290.0, 31.0, 0.7797284722328186, 1.0], [207.0, 263.0, 284.0, 300.0, 0.7650306224822998, 1.0], [471.0, 1.0, 544.0, 21.0, 0.7554300427436829, 1.0], [206.0, 327.0, 287.0, 370.0, 0.7211888432502747, 1.0], [524.0, 552.0, 570.0, 618.0, 0.7087181210517883, 1.0], [926.0, 241.0, 997.0, 266.0, 0.6508687138557434, 1.0], [208.0, 183.0, 250.0, 208.0, 0.6219822764396667, 1.0], [898.0, 0.0, 970.0, 12.0, 0.612953782081604, 1.0], [1029.0, 321.0, 1077.0, 354.0, 0.5040550827980042, 1.0], [648.0, 0.0, 716.0, 13.0, 0.4717086851596832, 1.0], [388.0, 342.0, 463.0, 422.0, 0.38127782940864563, 1.0], [651.0, 89.0, 724.0, 165.0, 0.37593430280685425, 1.0], [659.0, 330.0, 733.0, 413.0, 0.34557005763053894, 1.0], [207.0, 347.0, 280.0, 432.0, 0.3051230311393738, 1.0], [209.0, 124.0, 248.0, 157.0, 0.28398942947387695, 1.0], [531.0, 614.0, 565.0, 629.0, 0.24123512208461761, 1.0], [2.0, 275.0, 23.0, 336.0, 0.24044381082057953, 1.0], [207.0, 159.0, 243.0, 196.0, 0.21746589243412018, 1.0], [2.0, 679.0, 29.0, 720.0, 0.21233926713466644, 1.0], [1017.0, 227.0, 1052.0, 263.0, 0.21131367981433868, 1.0]]
  parking_lots = [[206, 41, 293, 75], [207, 101, 289, 131], [205, 212, 291, 245], [206, 268, 289, 302], [205, 330, 291, 361], [210, 385, 292, 420], [206, 448, 293, 481], [207, 508, 294, 541], [355, 534, 390, 631], [413, 532, 444, 628], [470, 529, 505, 626], [526, 528, 562, 625], [588, 526, 621, 619], [645, 519, 675, 616], [702, 516, 735, 614], [757, 513, 793, 611], [817, 510, 860, 606], [375, 28, 460, 61], [375, 67, 461, 100], [375, 104, 464, 139], [378, 143, 459, 178], [374, 183, 461, 215], [377, 220, 464, 256], [379, 260, 461, 301], [375, 304, 463, 337], [378, 343, 464, 380], [378, 382, 466, 420], [469, 381, 558, 420], [466, 338, 558, 378], [466, 297, 555, 337], [463, 253, 555, 297], [463, 213, 552, 258], [465, 176, 552, 217], [466, 135, 551, 176], [463, 96, 549, 138], [461, 58, 549, 96], [461, 19, 549, 59], [648, 371, 739, 409], [647, 327, 739, 371], [646, 287, 734, 325], [645, 246, 734, 286], [642, 205, 733, 247], [642, 169, 732, 206], [640, 128, 730, 171], [637, 89, 724, 128], [637, 53, 726, 85], [634, 16, 725, 50], [721, 13, 810, 53], [728, 52, 813, 87], [726, 89, 815, 129], [728, 127, 817, 164], [732, 164, 823, 203], [730, 203, 823, 246], [733, 248, 827, 284], [733, 282, 825, 321], [889, 11, 974, 48], [892, 50, 978, 87], [894, 85, 980, 126], [900, 125, 983, 166], [900, 166, 987, 203], [902, 201, 993, 240]]

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
import cv2
import pandas as pd


# save car bounding boxes to txt file
def save_car_info(cars,dest_path): 
    # car_bbx = cars[0].tolist()
    car_bbx = cars.tolist()
    pd_car_bbx = pd.DataFrame(car_bbx)
    # print(pd_car_bbx)
    pd_car_bbx = pd_car_bbx.drop([4,5], axis=1)


    pd_car_bbx.to_csv(dest_path,index=False,header=False)

def draw_rect(empty_slots,src_img,dest_img,total_space,empty_space):
    img = cv2.imread(src_img)   # image to draw on

    # draw empty slot 
    color = (0,255,0)   # yellow
    thickness = 3
    for slot in empty_slots:
        x1, y1, x2, y2 = slot
        img = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

    # to show how many vacant slots and total slots on the result image
    cv2.putText(img, "Available: %d spots" % empty_space, (30, 95),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 0, 0), 2)

    cv2.putText(img, "Total: %d spots" % total_space, (30, 125),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 0, 0), 2)
    
    cv2.imwrite(dest_img, img)


def yolo_to_org(input_path,img_w, img_h):   # from yolo format to orginal format(x1,x2,y1,y2)
                                                        # yolo format: (x_center,y_center,width,height). and is normalized to the range 0~1
  # get file with yolo format 
  fl = open(input_path, 'r')
  data = fl.readlines()
  fl.close()

  space_bbx = []
  for temp in data:
    _, x, y, w, h = map(float, temp.split(' ')) # the first value is not used(class id)
    x1 = int((x - w / 2) * img_w)
    x2 = int((x + w / 2) * img_w)
    y1 = int((y - h / 2) * img_h)
    y2 = int((y + h / 2) * img_h)
    
    if x1 < 0:
        x1 = 0
    if x2 > img_w - 1:
        x2 = img_w - 1
    if y1 < 0:
        y1 = 0
    if y2 > img_h - 1:
        y2 = img_h - 1
    # append each line to the list
    tmp = [x1, y1, x2, y2]
    space_bbx.append(tmp)
  #pd.DataFrame(space_bbx).to_csv(output_path,index=False,header=False)
  return space_bbx


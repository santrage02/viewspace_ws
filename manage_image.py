# -*- coding: utf-8 -*-
"""
manage_image.py
"""


import cv2
import numpy as np

def crop_image():
  img = cv2.imread('input.jpg') 
                                
  cv2.imshow(img)
  # Cropping an image
  x_size = 1280
  y_size = 720
  x_unit = 640
  y_unit = 320



  for j in range(0, y_size - y_unit//2, y_unit//2):
    for i in range(0, x_size - x_unit//2, x_unit//2):
      cropped_image = img[j:j+y_unit, i:i+x_unit]
      print(i, ' to ', i+x_unit, ' / ', j, ' to ', j+y_unit)
      cv2.imshow(cropped_image)
      cv2.imwrite("crop" + str(i) + str(j) + ".jpg", cropped_image)
      
  cv2.waitKey(0)
  cv2.destroyAllWindows()

"""# Capture Frames of a video"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

# import cv2
import os
from matplotlib import pyplot as plt


# cap = cv2.VideoCapture('/content/gdrive/MyDrive/Viewmagine_CV/datasets/Custom_dataset/parkinglot.mp4')
cap = cv2.VideoCapture('video/parkinglot_video.mp4')

'''
Try to change resolution of captured images. 
cap.set(cv2.CAP_PROP_FPS, 100)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'))
width = 1280
height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
'''

print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
count = 0
while cap.isOpened():
    if count == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        break;
            

    ret,frame = cap.read()
    # cv2.imwrite("/content/gdrive/MyDrive/Viewmagine_CV/datasets/Custom_dataset/parkinglot_capture_new/%d.png" % count, frame)
    cv2.imwrite("video/parkinglot_capture_new/%d.png" % count, frame)
    count = count + 1


    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() # destroy all opened windows


"""# Stitch image"""

# import cv2
# import os
# from matplotlib import pyplot as plt

path = 'video/parkinglot_capture_new'
images = []

for root, directories, files in os.walk(path):
    for file in files:
        if '00.png' in file:
            img_input =cv2.imread(os.path.join(root, file))
            images.append(img_input)
            plt.imshow(img_input)

print(len(images))

stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
status, pano = stitcher.stitch(images)

if status != cv2.Stitcher_OK:
    print("Can't stitch images, error code = %d" % status)
    sys.exit()
  
title = ""
cv2.imshow(title, pano)
cv2.imwrite('video/stitched.png', pano)
print("test")
# cv2.waitKey(0)
print("stitching completed successfully.")

"""# Rotate Image"""

# import cv2
# import numpy as np

# read image
src = cv2.imread("video/stitched.png")
old_image_height, old_image_width, channels = src.shape

# create new image of desired size and color (blue) for padding
new_image_width = 2500
new_image_height = 2500

# new_image_width = 2000
# new_image_height = 2000

color = (0,0,0)
result = np.full((new_image_height,new_image_width, channels), color, dtype=np.uint8)

# compute center offset
x_center = (new_image_width - old_image_width) // 2
y_center = (new_image_height - old_image_height) // 2

# copy img image into center of result image
result[y_center:y_center+old_image_height, 
       x_center:x_center+old_image_width] = src

height, width, channel = result.shape
matrix = cv2.getRotationMatrix2D((width/2, height/2), 30, 1)
dst = cv2.warpAffine(result, matrix, (width, height))

cv2.imshow(title, dst)
cv2.imwrite("video/rotated.png", dst)

# cv2.waitKey()
cv2.destroyAllWindows()
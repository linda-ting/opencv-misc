import cv2
import numpy as np

# get face cascade
face_cascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")

# read from webcam
video = cv2.VideoCapture(0)

# set up points to be drawn
points = []
draw = True

# set up pen color
colors = []
pen_color = [0,0,0]

"""
update values of r,g,b channels of pen_color, respectively
"""
def change_red(num):
  pen_color[2] = num

def change_green(num):
  pen_color[1] = num

def change_blue(num):
  pen_color[0] = num

"""
create canvas window & trackbars to pick pen color
"""
cv2.namedWindow("Canvas")
cv2.resizeWindow("Canvas", 500, 100)
cv2.createTrackbar("Red", "Canvas", 0, 255, change_red)
cv2.createTrackbar("Green", "Canvas", 0, 255, change_green)
cv2.createTrackbar("Blue", "Canvas", 0, 255, change_blue)

"""
redraws all stored points onto canvas
"""
def drawPoints(points):
  for i in range(1, len(points)):
    if points[i-1] is None or points[i] is None:
      break
    pt1 = (points[i-1][0], points[i-1][1])
    pt2 = (points[i][0], points[i][1])
    color = (colors[i][0], colors[i][1], colors[i][2])
    cv2.line(imgCanvas, pt1, pt2, color, 3)

"""
loops through frames captured by webcam
"""
while True:
  success, img = video.read()
  img = cv2.resize(img, (640,360))
  imgCanvas = img.copy()
  
  # draw instructional text
  cv2.putText(imgCanvas, "press 'c' to CLEAR", (5, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)  
  cv2.putText(imgCanvas, "press 'v' to LIFT/DRAW", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
  cv2.putText(imgCanvas, "press 'q' to QUIT", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)  

  # find the largest/closest face to draw with
  faces = face_cascade.detectMultiScale(img, 1.1, 4)
  max_area = 0
  for (x,y,w,h) in faces:
    area = w*h
    if area > max_area:
      (this_x, this_y, this_w, this_h) = (x,y,w,h)
      max_area = area

  cv2.rectangle(imgCanvas, (this_x,this_y), (this_x+this_w,this_y+this_h), (0,255,255), 1)

  if draw:
    points.append([this_x+this_w//2,this_y+this_h//2])
    colors.append([pen_color[0], pen_color[1], pen_color[2]])

  # redraw all points
  drawPoints(points)
  cv2.imshow("Canvas", imgCanvas)

  key = cv2.waitKey(1) & 0xFF

  # quit if 'q' is pressed
  if key == ord('q'):
    break

  # clear canvas if 'c' is pressed
  elif key == ord('c'):
    points = []
    colors = []
  
  # toggle draw mode if 'v' is pressed
  elif key == ord('v'):
    draw = not draw

# close all windows
video.release()
cv2.destroyAllWindows()
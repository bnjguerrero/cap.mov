import cv2
import requests
import sys
from datetime import datetime, date, time, timedelta


deteccion = True;
camara = 0;
ahora=datetime.now()

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 2):
    for x, y, w, h in rects:
        pad_w, pad_h = int(0.18*w), int(0.08*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)




def alerta():
      id = "618709347"
 
      token = "576479005:AAHODRk1MsFU6qpOxz9JAu1vH_PxppBrh_g"
 
      url = "https://api.telegram.org/bot" + token + "/sendMessage"
      params = {
      'chat_id': id,
 
      'text' : "Alerta",
      }
      requests.post(url, params=params)
      


cap = cv2.VideoCapture();



nombreven = "SecurCam"; 


if (((len(sys.argv) == 2) and (cap.open(str(sys.argv[1]))))
    or (cap.open(camara))):


    cv2.namedWindow(nombreven, cv2.WINDOW_NORMAL);


    hog = cv2.HOGDescriptor();
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() );

    while (deteccion):


        if (cap.isOpened):
            ret, img = cap.read();



        found, w = hog.detectMultiScale(img,winStride=(4, 4),padding=(8, 8), scale=1.05)
        found_filtered = []

        for ri, r in enumerate(found):
            for qi, q in enumerate(found):
                if ri != qi and inside(r, q):
                    break
                else:
                    found_filtered.append(r)
                    if ahora<datetime.now(): 
                    	alerta()
                    	ahora=ahora+timedelta(minutes=1)

        draw_detections(img, found_filtered, 3)

        cv2.imshow(nombreven,img);


        key = cv2.waitKey(60) & 0xFF;
        if (key == ord('q')):
            deteccion = False;


    cv2.destroyAllWindows()

else:

     print("La camara no esta conectada.")
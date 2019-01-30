# -*- coding:utf-8 -*-
import cv2
import os 
import time
from face_pp import facepp
from dingtalk_message import DingtalkMsg

def get_time():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime('%Y_%m_%d_%H_%M_%S', local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = '%s_%03d'%(data_head, data_secs)
    return time_stamp


def get_timestamp(s=None):
    if s is None:
        t = time.time()
    else:
        t = time.mktime(time.strptime(s[:-4],'%Y_%m_%d_%H_%M_%S'))
    return int(t) 


def main():
    # recognizer = cv2.face.LBPHFaceRecognizer_create()
    # recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    f = facepp()
    dm = DingtalkMsg()
    # show_camera = True
    show_camera = False

    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0

    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'Wyn', 'Miffywarm'] 

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 1280) # set video widht
    cam.set(4, 960) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    while True:
        ret, img =cam.read()
        # img = cv2.flip(img, -1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )

        time_stamp = get_time()
        if len(faces) > 0:
            filename = "dataset/alert_%s.jpg"%(time_stamp)
            print("[INFO] face in picture, saving as '%s' and calling face++ web api..."%filename)
            cv2.imwrite(filename, img)

            res_f = f.is_homemate(filename)

            if res_f is None:
                os.system("rm -f %s"%filename)
            elif f.is_homemate(filename):
                os.system("rm -f %s"%filename)
            else:
                msg = "[Warning] 有陌生人进入！已存入图片%s！"%filename
                print(msg)
                dm.send(msg)
                q.put(time_stamp)
            time.sleep(0.2)

        # for (x,y,w,h) in faces:

        #     cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        #     id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        #     # Check if confidence is less them 100 ==> "0" is perfect match 
        #     if (confidence < 100):
        #         id = names[id]
        #         confidence = "  {0}%".format(round(100 - confidence))
        #     else:
        #         id = "unknown"
        #         confidence = "  {0}%".format(round(100 - confidence))
        
        #     cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        #     cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  

        if show_camera:
            cv2.imshow('camera',img) 

        k = cv2.waitKey(30) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

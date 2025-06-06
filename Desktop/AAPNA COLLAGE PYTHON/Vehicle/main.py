import cv2
import numpy as np 



#webcamera

cap = cv2.VideoCapture('video.mp4')
min_width_react = 80 #minimum width rectangle 
min_height_react = 80 # minimum height rectangle 




#Intialize Subtractor 

algo = cv2.bgsegm.createBackgroundSubtractorMOG()

def center_point (x,y,w,h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx ,cy



detect = [ ]
offset = 6 # allowable error to 6
countre = 0





while True:
    ret , frame1 = cap.read()
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    # apply to all frame

    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel =cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilit = cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)
    dilit = cv2.morphologyEx(dilit,cv2.MORPH_CLOSE,kernel)
    counter,h  = cv2.findContours(dilit,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    count_line_position = 550

    count_line = cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(255,127,0),3)
  
    #cv2.imshow(" Detector ",dilit)



    for (i,c) in enumerate(counter):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>=min_width_react)and (h>=min_height_react)
        if not validate_counter:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)


        center = center_point(x,y,w,h)
        detect.append(center)


        cv2.circle(frame1,center,4,(0,0,255),-1)


        remove_list = [ ]
        for(x,y ) in detect :
            if (count_line_position-offset)< y <(count_line_position+offset):
                countre +=1
            remove_list.append((x,y))
            cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(0,127,255),3)
            
            print("vehile counter : "+str(countre))
        for pt in remove_list:
            detect.remove(pt)

    cv2.putText(frame1,"vehicle counter :"+str(countre),(450,70),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255))


    cv2.imshow("video Orignal ",frame1)

    if cv2.waitKey(1) == 13 :
        break 
cv2.destroyAllWindows()
cap.release()


'''
Created on Oct 4, 2019

@author: thelunararmy
'''

import numpy as np
import cv2
from OpenCVExtended import *
import time
import mss
import datetime

# This is on my second monitor so need to move the bounding box away from the first 
# Monitor 1: 1680x1050
# Monitor 2: 1366x768
monitor = {"top": 1050-768+190, "left": 1680+250, "width": 850, "height": 475}

# Some statics!
kernel = cv.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
size_to_capture = 300
threshold_min = 30
min_rect_size = 10
blur_size = 9

# Dont flood my PC with images while I sleep!
IMAGE_MAX = 500


def screen_record(): 
    with mss.mss() as sct:
        last_time = time.time() # A timer to monitor FPS, disabled once working
        o1 = None # the first frame of the video which will act as out "starting" image
        timer = 0 # frame time
        image_counter = 0 # max counter
        last_known_capture = "Last Sighting: Nothing yet :(" 
        last_known_image = np.zeros((size_to_capture,size_to_capture,3),np.uint8)
        while(True):
            timer += 1
            timer = timer % 120 # reset every X frames
            # 800x600 windowed mode
            printscreen = np.array(sct.grab(monitor)) # fetch video image
            printscreen = cv.cvtColor(printscreen,cv.COLOR_RGBA2RGB) # remove alpha channel
            printscreen2 = RescaleImageToHeight(printscreen, size_to_capture) # reduce size
            gray = cv.cvtColor(printscreen2,cv.COLOR_RGB2GRAY) # convert to grayscale
            gray = cv.GaussianBlur(gray,(blur_size,blur_size),0)
            if (o1 is None): o1 = gray # set the first capture frame to the OG frame for difference
            
            diff = np.zeros((1,1,3),np.uint8) # some blank images
            debug = np.zeros((1,1,3),np.uint8)
            
            if o1 is not None:  # do motion detection
                diff = cv.absdiff(gray,o1) # subtracts OG frame from current frame
                
                ret,thresh = cv.threshold(diff,threshold_min,255,0) # find movement and remove noise 
                thresh = cv.morphologyEx(thresh, cv.MORPH_DILATE, kernel,iterations=3) 
                debug = thresh.copy()
                _, contours, _ = cv.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # isolate movement
                diff = printscreen2.copy()
                found = 0 # count how many movement pieces we found
                for c in contours:
                    rect = cv2.boundingRect(c) # create box around movement
                    if rect[2] < min_rect_size or rect[3] < min_rect_size: continue # check to see if movement is greater than a specific size
                    # at this point we found something!
                    found += 1 # increase counter                    
                    x,y,w,h = rect
                    cv2.rectangle(diff,(x,y),(x+w,y+h),(255,0,255),3) # draw a box on the image
                
                if found > 0: # we found something! yell, scream, party!
                    d = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
                    print image_counter, "I FOUND SOMETHING! It happened at:", d
                    image_counter +=1 
                    last_known_capture = "Last Sighting: %s" % d
                    last_known_image = diff
                    
                    # Merged image
                    
                    tinydiff = RescaleImageToHeight(diff, 100)
                    tinydebug = RescaleImageToHeight(debug, 100)
                    '''
                    merged = printscreen.copy()
                    tinyH,tinyW,_ = tinydiff.shape
                    mergH,mergW,_ = merged.shape
                    merged[mergH-tinyH:mergH,mergW-tinyW:mergW] = tinydiff   
                    '''
                    merged = ImagePhalanx([printscreen,ImageVertigo([tinydiff,tinydebug])],2)        
                    
                    # save images to device
                    d = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    cv.imwrite("found/HD/"+d+"_"+"%d"%image_counter+"_HD.png",merged)
                    # cv.imwrite("found/"+d+".png",ImageVertigo([diff]))
            
            if image_counter > IMAGE_MAX:
                print "Reached IMAGE MAX at", datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
                quit()    
                         
            # display the video feeds
            resultimg = NamedImageCatalog([(printscreen2,"Livefeed"),
                                           (debug,"Detecting Movement"), 
                                           (diff,"Tracking Feed"),
                                           (last_known_image,last_known_capture)], 2,2,(0,0,0))
            
            
            #@print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            # handle screen
            cv2.imshow('Videotracker Press Q to Stop',resultimg)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        
if __name__ == '__main__':
    screen_record() # gogogo!



import cv2 as cv    # OpenCV    
import numpy as np  # NumPy

def ImagePhalanx (images,linewidthbetween=0,bgcol=(0,0,0)):
    '''
    Creates a composite image using a list of image objects, with an optional line space in between and background colour. Horizontal arrangement.
    '''
    if len (images) <= 0:
        print "ImagePhalanx was given an empty list!"
        return np.zeros((1,1,3),np.uint8)
    else:
        maxHeight = max([i.shape[0] for i in images])
        totalWidth = sum([i.shape[1] for i in images]) + linewidthbetween * (len(images) - 1) 
        returnImage = np.zeros((maxHeight,totalWidth,3),np.uint8)
        returnImage[:] = bgcol
        runningWidth = 0
        for i in range(len(images)):
            img = images[i] if images[i].ndim == 3 else cv.cvtColor(images[i],cv.COLOR_GRAY2BGR)
            currH, currW = img.shape[:2]
            returnImage[0:currH,runningWidth:runningWidth+currW] = img
            runningWidth += currW + linewidthbetween
        return returnImage


def ImageVertigo (images,linewidthbetween=0,bgcol=(0,0,0)):
    '''
    Creates a composite image using a list of image objects, with an optional line space in between and background colour. Vertical arrangement.
    '''
    if len (images) <= 0:
        print "ImageVertigo was given an empty list!"
        return np.zeros((1,1,3),np.uint8)
    else:
        maxWidth = max([i.shape[1] for i in images])
        totalHeight = sum([i.shape[0] for i in images]) + linewidthbetween * (len(images) - 1) 
        returnImage = np.zeros((totalHeight,maxWidth,3),np.uint8)
        returnImage[:] = bgcol
        runningHeight = 0
        for i in range(len(images)):
            img = images[i] if images[i].ndim == 3 else cv.cvtColor(images[i],cv.COLOR_GRAY2BGR)
            currH, currW = img.shape[:2]
            returnImage[runningHeight:runningHeight+currH,0:currW] = img
            runningHeight += currH + linewidthbetween
        return returnImage
    
    
def ImageCatalog (images,imagesPerRow= 0,linewidthbetween=0,bgcol=(0,0,0)):
    '''
    Creates a composite image using a list of image objects, with an optional line space in between and background colour. Grid arrangement.
    '''
    if len (images) <= 0:
        print "ImageCatalog was given an empty list!"
        return np.zeros((1,1,3),np.uint8)
    else:
        imagesPerRow = int( len (images) / 2 ) if (imagesPerRow < 1) else imagesPerRow
        finalToBeVertigo = []
        runningPool = []
        for idx,img in enumerate(images):
            if ( idx == (len(images)-1) ) or ( (idx+1) % imagesPerRow == 0 ):
                runningPool.append(img)
                finalToBeVertigo.append(ImagePhalanx(runningPool, linewidthbetween, bgcol))
                del runningPool [:]
            else:
                runningPool.append(img)
        return ImageVertigo(finalToBeVertigo, linewidthbetween, bgcol)  


def ImageNaming (image, text, text_scale= 1.0,color = (255,255,255)):
    '''
    Prints the given text on top of the an image.
    '''
    boxpadding = int(np.ceil((20.0) * (text_scale / 1.0)))
    h, w = image.shape[:2]
    h2 = h+boxpadding
    returnImage = np.zeros((h2,w,3),np.uint8)
    img = image if image.ndim == 3 else cv.cvtColor(image,cv.COLOR_GRAY2BGR)
    returnImage[boxpadding:h2,0:w] = img
    cv.putText(returnImage,text,(3,int(boxpadding-5)),cv.FONT_HERSHEY_PLAIN,text_scale,color) 
    return returnImage


def NamedImageCatalog (imagesWithNames,imagesPerRow= -1,linewidthbetween=0,bgcol=(0,0,0),text_scale=1.0,textcol = (255,255,255)):
    '''
    Creates a composite image using a list of image objects, with an optional line space in between and background colour. Grid arrangement withe very frame named.
    '''
    if len(imagesWithNames) == 0 or len(imagesWithNames[0]) != 2:
        print "NamedImageCatalog was either an empty imagesWithNames list or invalid pairings!"
        return np.zeros((1,1,3),np.uint8)
    else:
        toBeCataloged = []
        for image,name in imagesWithNames:
            toBeCataloged.append(ImageNaming(image,name,text_scale,textcol))
        return ImageCatalog(toBeCataloged, imagesPerRow, linewidthbetween, bgcol)
      
def RescaleImage (image,factor,method = cv.INTER_CUBIC ):
    '''
    Resizes an image by a factor
    '''
    return cv.resize(image,(int(image.shape[1]*factor*1.0),int(image.shape[0]*factor*1.0) ),0,0,interpolation=method)


def RescaleImageToHeight (image,height, method = cv.INTER_CUBIC):
    '''
    Resizes an image to a given height, keeping its aspect ratio locked
    '''
    heightRatio = 1.0 * height / image.shape[0] 
    return cv.resize(image,(int(image.shape[1]*heightRatio*1.0),int(image.shape[0]*heightRatio*1.0) ),0,0,interpolation=method)


def RescaleImageToHeightWidth (image,height,width,method = cv.INTER_CUBIC):
    '''
    Resized an image to a given height and width, regardless of its aspect ratio
    '''
    return cv.resize(image,(width,height),0,0,interpolation=method)


def CenterPointOfContour(theContour):
    '''
    Attempts to find the center point of a given contour, if it fails then it returns (-1,-1)
    '''
    try:
        M = cv.moments(theContour)
        return int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    except:
        return -1,-1


def DebugPointer (image):
    '''
    Displays the image in a window and then ends the program afterwards
    '''
    cv.imshow("Debug out",ImagePhalanx([image]))
    cv.waitKey(0)
    cv.destroyAllWindows()
    quit()
    
def RescaleAllImagesToHeight(images,height,method = cv.INTER_CUBIC):
    return [RescaleImageToHeight(img, height,method) for img in images]


def SimpleWebcamFeed(src=0,debugText=False):
    cam = cv.VideoCapture(src)
    ret, frame = cam.read()
    while ret:
        ret, frame = cam.read()
        if debugText: 
            frame = ImageNaming(frame, "Press Q to exit", 0.8)
        cv.imshow("Simple Window",frame)
        k = cv.waitKey(1)
        if k == ord('q'):
            break
    cv.destroyWindow("Simple Window")
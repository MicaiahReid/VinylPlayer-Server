# pylint: skip-file
import cv2
import matplotlib.pyplot as plt
import numpy as np

minArea = 128
maxArea = 6144

def segment(img, img_height, img_width):
    img = cv2.resize(img, (img_height, img_width))
    
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, 3, 7, 21)
    
    if img is None:
        print("Image is null")
        return
    
    print("Original:")
    plt.imshow(rgb)
    plt.axis("off")
    plt.show()
    
    # convert to grayscale
    print("Image after grayscale:")
    plt.imshow(gray, cmap='gray')
    plt.axis("off")
    plt.show()
    
    # apply thresholding
    thresh = adaptiveThreshold(gray)
    
    # apply erosion & diliation
    kernel = np.ones((3,9), np.uint8)
    # eroded = erode(thresh, kernel)
    dilated = dilate(thresh, kernel)
    eroded = erode(dilated, kernel)
    dilated_2 = dilate(eroded, kernel)
    eroded_2 = erode(dilated_2, kernel)
    
    # find contours on image & draw bounding box
    gray, contours = findContours(eroded_2)
    rgb = drawBoundingBox(rgb, contours)
    
    
    
def adaptiveThreshold(gray):
    print("Image after thresholding:")
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 3)
    plt.axis("off")
    plt.imshow(thresh, cmap='gray')
    plt.show()
    return thresh

def erode(img, kernel):
    eroded = cv2.erode(img, kernel, iterations=1)
    print("Image after erosion:")
    plt.axis("off")
    plt.imshow(eroded, cmap='gray')
    plt.show()
    return eroded

def dilate(img, kernel):
    dilated = cv2.dilate(img, kernel, iterations=1)
    print("Image after diliation:")
    plt.axis("off")
    plt.imshow(dilated, cmap='gray')
    plt.show()
    return dilated

def findContours(img):
    image2, contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, contours, -1, (0,255,0), 4)

    print("Contours on image")   
    plt.axis("off")
    plt.imshow(img, cmap='gray')
    plt.show()
    return img, contours

def drawBoundingBox(img, contours):
    print("Bounding box on image")
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        x,y,w,h = cv2.boundingRect(contour)
        # print(area)
        if area < minArea or area > maxArea or w < h:
            continue
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
    plt.axis("off")
    plt.imshow(img)
    plt.show()
    return img  

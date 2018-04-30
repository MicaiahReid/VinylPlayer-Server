# pylint: skip-file
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def segment_image_v2(img, img_width=1024, img_height=512, min_contour_area=1200):
    height, width, channels = img.shape
    start_height = int(height - height*.7)
    end_height = int(height*.7)
    img = img[start_height:end_height, :]
    img = cv2.resize(img, (img_width, img_height))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # denoise
    gray = cv2.fastNlMeansDenoising(gray, h=3, templateWindowSize=7, searchWindowSize=21)
    
    if img is None:
        # print("Image is null")
        return [] 
    
    print("Original:")
    plt.imshow(rgb)
    plt.axis("off")
    plt.show()
    
    # convert to grayscale
    # print("Image after grayscale:")
    # plt.imshow(gray, cmap='gray')
    # plt.axis("off")
    # plt.show()
    
    # apply thresholding
    thresh = adaptive_threshold_image_v2(gray)
    
    # apply erosion & diliation
    kernel = np.ones((3,25), np.uint8)
    dilated = dilate_image_v2(thresh, kernel)
    eroded = erosion_image_v2(dilated, kernel)
    
    # find contours on image & draw bounding box
    rgb, contours = find_contours_image_v2(eroded, rgb, min_contour_area)
    segments = segment_using_contours_v2(img, contours)
    return segments

def segment_line_v2(img, img_height=1024, img_width=512, min_contour_area=4096):
    img = cv2.resize(img, (img_height, img_width))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if img is None:
        # print("Image is null")
        return
    
    # apply thresholding
    thresh = adaptive_threshold_line_v2(gray)
    
    # apply erosion & diliation
    kernel = np.ones((11,3), np.uint8)
    dilated = dilate_image_v2(thresh, kernel)
    eroded = erosion_image_v2(dilated, kernel)
    
     # find contours on image & draw bounding box
    rgb, contours = find_contours_image_v2(eroded, rgb, min_contour_area, sort_top_to_bottom=False)
    segments = segment_using_contours_v2(img, contours)
    return segments

def adaptive_threshold_image_v2(img):
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 3)
    # print("Image after thresholding:")
    # plt.axis("off")
    # plt.imshow(thresh, cmap='gray')
    # plt.show()
    return thresh

def adaptive_threshold_line_v2(img):
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 3)
    # print("Image after thresholding:")
    # plt.axis("off")
    # plt.imshow(thresh, cmap='gray')
    # plt.show()
    return thresh

def dilate_image_v2(img, kernel):
    dilated = cv2.dilate(img, kernel, iterations=1)
#    print("Image after diliation:")
#    plt.axis("off")
#    plt.imshow(dilated, cmap='gray')
#    plt.show()
    return dilated

def erosion_image_v2(img, kernel):
    eroded = cv2.erode(img, kernel, iterations=1)
#    print("Image after erosion:")
#    plt.axis("off")
#    plt.imshow(eroded, cmap='gray')
#    plt.show()
    return eroded

def filter_contours_image_v2(img, contours, hierarchy, min_area):
    # print("Filter Contours Image")
    filtered_contours = []
    if hierarchy is None:
        return img, []
    
    hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        x,y,w,h = cv2.boundingRect(contour)
        current_hierarchy = hierarchy[i]
        if area < min_area:
            continue

        if np.any(current_hierarchy[3] > 0):
            continue
        
        filtered_contours.append(contour)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    # plt.axis("off")
    # plt.imshow(img)
    # plt.show()
    return img, filtered_contours

def find_contours_image_v2(img, rgb, min_area, sort_top_to_bottom=True):
    image2, contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0,255,0), 4)
    if contours is None:
        return img, []

    rgb, contours = filter_contours_image_v2(rgb, contours, hierarchy, min_area)
    if len(contours) <= 0:
        return img, []
    
    # sort contours 
    contours = sort_contours_image_v2(contours, method="left-to-right")
    if sort_top_to_bottom:  
        contours = sort_contours_image_v2(contours, method="top-to-bottom")
    return img, contours

def segment_using_contours_v2(img, contours):
    segments = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        segment = img[y:y+h, x:x+w]
    
        # plt.imshow(segment, cmap='gray')
        # plt.axis("off")
        # plt.show()
        
        segments.append(segment)   
    return segments

def sort_contours_image_v2(contours, method="left-to-right"):
    reverse = False
    i = 0
    
	# handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
 
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
 
	# construct the list of bounding boxes and sort them from top to bottom
    boundingBoxes = [cv2.boundingRect(contour) for contour in contours]
    contours, boundingBoxes = zip(*sorted(zip(contours, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
     
    return list(contours)
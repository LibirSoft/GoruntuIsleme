import cv2
import numpy as np
import os
from statistics import mean
from os import listdir
from os.path import isfile, join

path = "/home/libir/Desktop/thesis/Example-images/PureImages/TO"
cleared_path = "/home/libir/Desktop/thesis/Example-images/CleanedImages/Cleaned_TO"

imagelist = [f for f in listdir(path) if isfile(join(path, f))]

print(imagelist)

avg_area2 = []

for image_name in imagelist:
    print(image_name)
    img = cv2.imread(path + "/" + image_name)

    mask_all = cv2.inRange(img, np.array([0, 10, 0]), np.array([255, 255, 255]))
    thresh = mask_all

    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

    kernel = np.ones((6, 6), np.uint8)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

    ret, thresh2 = cv2.threshold(closing, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    blur = cv2.blur(thresh2, (15, 15))

    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)

    rect_areas = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        rect_areas.append(w * h)
    avg_area = mean(rect_areas)
    avg_area2.append(avg_area)

for image_name in imagelist:
    print(image_name)
    img = cv2.imread(path + "/" + image_name)

    mask_all = cv2.inRange(img, np.array([0, 10, 0]), np.array([255, 255, 255]))
    thresh = mask_all

    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

    kernel = np.ones((6, 6), np.uint8)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

    ret, thresh2 = cv2.threshold(closing, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    blur = cv2.blur(thresh2, (15, 15))

    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)

    rect_areas = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        rect_areas.append(w * h)
    avg_area = mean(rect_areas)
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cnt_area = w * h
        print("cnt area: " + str(cnt_area), "wanted area: " + str(1 * avg_area))
        if cnt_area < 1 * mean(avg_area2):
            thresh[y:y + h, x:x + w] = 0

    res = cv2.bitwise_and(img, img, mask=thresh)

    cv2.imwrite(os.path.join(cleared_path, "Cleaned_" + image_name), res)

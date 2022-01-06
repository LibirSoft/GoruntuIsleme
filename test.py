import cv2
import numpy as np
import os
from statistics import mean
from os import listdir
from os.path import isfile, join

path = "/home/libir/Desktop/thesis/Example-images/PureImages/S2"
cleared_path = "/home/libir/Desktop/thesis/Example-images/CleanedImages/Jpeg"

# Klasördeki görüntüler alınıyor
imagelist = [f for f in listdir(path) if isfile(join(path, f))]

for image_name in imagelist:
    img = cv2.imread(path + "/" + image_name)
    image_name = image_name.split(".")[0]
    img_to_show = img;

    # eliminating red channel
    # img[:,:,2] = 0

    #######İncir alanını bulmak için görüntünün tamamı maskeleniyor.
    mask_all = cv2.inRange(img, np.array([0, 10, 0]), np.array([255, 255, 255]))
    thresh = mask_all

    # Acinimla gurultu sil. Once erode sonra dilation
    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

    # Resim ici maskelenmeyen yerler icin kapanim
    kernel = np.ones((6, 6), np.uint8)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Kucuk noktalari sil
    ret, thresh2 = cv2.threshold(closing, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Bulaniklastir
    blur = cv2.blur(thresh2, (15, 15))
    # Kucuk noktalari sil
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

        if cnt_area < 1 * avg_area:
            thresh[y:y + h, x:x + w] = 0

    res = cv2.bitwise_and(img, img, mask=thresh)
    # imgHSV = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)

    #    cv2.namedWindow(image_name + "_Original Image",cv2.WINDOW_NORMAL)
    #    cv2.resizeWindow(image_name + "_Original Image", 460,328)
    #    cv2.imshow(image_name + "_Original Image",thresh)

    #    cv2.namedWindow(image_name + "_Masked Image",cv2.WINDOW_NORMAL)
    #    cv2.resizeWindow(image_name + "_Masked Image", 460,328)
    #    cv2.imshow(image_name + "_Masked Image",res)

    cv2.imwrite(os.path.join(cleared_path, image_name + '_cleaned.jpg'), res)

cv2.waitKey(0)
cv2.destroyAllWindows()

import os
from os import listdir
from os.path import isfile, join
import cv2

path = "/home/libir/Desktop/thesis/Example-images/CleanedImages/Cleaned_TO"
cleared_path = "/home/libir/Desktop/thesis/Example-images/CleanedImages/Croped_TO"

imagelist = [f for f in listdir(path) if isfile(join(path, f))]
i = 0
for image_name in imagelist:
    print(image_name)
    img = cv2.imread(path + "/" + image_name)

    x = img.shape[1]
    print(x)
    y = img.shape[0]
    print(y)

    croped_1 = img[0:int(y / 2), 0:int(x / 2)]
    croped_2 = img[0:int(y / 2), int(x / 2):int(x)]
    croped_3 = img[int(y / 2):y, 0:int(x / 2)]
    croped_4 = img[int(y / 2):y, int(x / 2):x]

    cv2.imwrite(os.path.join(cleared_path, "Croped_" + str((i * 4) + 1) + "_" + image_name), croped_1)
    cv2.imwrite(os.path.join(cleared_path, "Croped_" + str((i * 4) + 2) + "_" + image_name), croped_2)
    cv2.imwrite(os.path.join(cleared_path, "Croped_" + str((i * 4) + 3) + "_" + image_name), croped_3)
    cv2.imwrite(os.path.join(cleared_path, "Croped_" + str((i * 4) + 4) + "_" + image_name), croped_4)
    i = i + 1

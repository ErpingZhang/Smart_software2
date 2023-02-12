import cv2
import os
import datetime
import numpy


img_item = numpy.empty(10, dtype=object)
img_loca = numpy.empty(10, dtype=object)


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.mkdir(directory)
    except OSError:
        print('Error')
    try:
        if not os.path.exists(directory+r'\item'):
            os.mkdir(directory+r'\item')
    except OSError:
        print('Error')
    try:
        if not os.path.exists(directory + r'\location'):
            os.mkdir(directory + r'\location')
    except OSError:
        print('Error')


def frameStorage(directory, itemNum, item, location, key):

    fileName = ""
    current_time = datetime.datetime.now()
    t = current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second, current_time.microsecond

    for i in range(len(t)):
        fileName = fileName + '_' + str(t[i])

    if key == 'i':
    # SPACE pressed
        path1 = directory + r'\item'
        img_item[itemNum] = "item{}.png".format(itemNum)
        cv2.imwrite(os.path.join(path1, img_item[itemNum]), item)
        print("{} written!".format(img_item[itemNum]))

        path2 = directory + r'\location'
        img_loca[itemNum] = "item{}".format(itemNum) + "_" + "frame{}.png".format(fileName)
        cv2.imwrite(os.path.join(path2, img_loca[itemNum]), location)
        print("{} written!".format(img_loca[itemNum]))
    elif key == 'u':
        path2 = directory + r'\location'
        rpath = os.path.join(path2, img_loca[itemNum])
        os.remove(rpath)
        img_loca[itemNum] = "item{}".format(itemNum) + "_" + "frame{}.png".format(fileName)
        cv2.imwrite(os.path.join(path2, img_loca[itemNum]), location)
        print("{} written!".format(img_loca[itemNum]))



'''

createFolder()
frameStorage(1,'i')
frameStorage(1,'u')
frameStorage(2,'i')
frameStorage(9,'i')
frameStorage(9,'u')
'''


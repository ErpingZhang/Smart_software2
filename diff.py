import numpy as np
import cv2
from skimage.metrics import structural_similarity as compare_ssim
import os
from save_image import *

def mse(img1, img2):
   h, w = img1.shape
   diff = cv2.subtract(img1, img2)
   err = np.sum(diff**2)
   mse = err/(float(h*w))

   '''
   cv2.imshow("1",diff)
   cv2.imshow("2", img1)
   cv2.imshow("3", img2)
   cv2.waitKey(0)
   '''
   print(mse)

   return mse


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images


def find_contour(img):
    thresh = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((7, 7), np.uint8)
    img_close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    img_Gaussian = cv2.GaussianBlur(img_close, (7, 7), 0)
    cnts, hierarchy = cv2.findContours(img_Gaussian.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    return contours


def item_match(item, img):
    orb = cv2.ORB_create()
    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(item, None)
    kp2, des2 = orb.detectAndCompute(img, None)
    # create BFMatcher object
    bf = cv2.BFMatcher()
    # Match descriptors.

    # Sort them in the order of their distance.
    matches = bf.knnMatch(des1, des2, k=2)

    good = []

    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good.append([m])

    if len(good) >= 6:
        '''
        # Draw first 10 matches.
        img3 = cv2.drawMatchesKnn(item, kp1, testImg, kp2, good, None,
                                  flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow("result", img3)
        cv2.waitKey(0)
        cv2.imwrite(os.path.join(path, "match1.jpg"), img3)
        '''

        return True
    else:
        print("object not found")
        return False


def item_comp(itemList1, itemList2,img_list,img):
    first_range = len(itemList1)
    second_range = len(itemList2)
    if first_range == 0:
        loc_list = [0 for x in range(second_range)]
        for i in range(second_range):
            itemList1.append(itemList2[i])
            loc_list[i] = img_list[i]
    elif second_range == 0:
        loc_list = [0 for x in range(first_range)]
        for i in range(first_range):
            loc_list[i] = img
    else:
        loc_list = [0 for x in range(first_range)]
        for i in range(second_range):
            for j in range(first_range):
                if item_match(itemList2[i],itemList1[j]):
                    loc_list[j] = img_list[i]
                    print("yes")
                else:
                    itemList1.append(itemList2[i])
                    loc_list.append(img_list[i])
    return itemList1, loc_list


def extract_item(path, orimg1, orimg2):
    before_item = []
    current_item = []
    img_list = []
    img1 = cv2.cvtColor(orimg1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(orimg2, cv2.COLOR_BGR2GRAY)
    img1 = cv2.GaussianBlur(img1, (7, 7), 0)
    img2 = cv2.GaussianBlur(img2, (7, 7), 0)
    diff = cv2.absdiff(img2, img1)

    thresh = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)[1]
    
    cv2.imwrite(path+'image3.jpg',diff)
    kernel = np.ones((9, 9), np.uint8)
    img_open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    img_close = cv2.morphologyEx(img_open, cv2.MORPH_CLOSE, kernel)
    #img_open = cv2.morphologyEx(img_close,cv2.MORPH_OPEN,kernel)
    img_Gaussian = cv2.GaussianBlur(img_close, (7, 7), 0)
    cv2.imwrite(path+'image4.jpg',img_Gaussian)
    cnts, hierarchy = cv2.findContours(img_Gaussian.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = []
    check = []

    for a in cnts:

        if cv2.contourArea(a) > 3000:
            check.append(a)
    for b in check :
        flag = 0
        (x1,y1,w1,h1) = cv2.boundingRect(b)
        for b2 in check:
            (x2, y2, w2, h2) = cv2.boundingRect(b2)
            if x1 > x2 and x1 < x2+w2:
                flag = 1
                break
        if flag == 0:
            contours.append(b)
    for c in contours:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        item1 = orimg1[y:y + h, x:x + w]
        item2 = orimg2[y:y + h, x:x + w]
        grey_item1 = cv2.cvtColor(item1, cv2.COLOR_BGR2GRAY)
        grey_item2 = cv2.cvtColor(item2, cv2.COLOR_BGR2GRAY)
        item = cv2.absdiff(item1,item2)
        score1, diff1 = compare_ssim(item1, item, multichannel=True, full=True, data_range=255)
        score2, diff2 = compare_ssim(item2, item, multichannel=True, full=True, data_range=255)
        print(score1,score2)
        #if mse(grey_item1,item) > mse(grey_item2,item):
        if score2 > score1:
            #cv2.rectangle(loc_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            #cv2.imwrite(os.path.join(path, "r2.jpg"), item2)
            before_item.append(item1)

        else:
            #
            #cv2.imwrite(os.path.join(path, "r1.jpg"), item1)
            current_item.append(item2)
            loc_image = orimg2.copy()
            cv2.rectangle(loc_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            img_list.append(loc_image)


        #print(cv2.contourArea(c))
        #cv2.rectangle(orimg2, (x, y), (x + w, y + h), (0, 0, 255), 2)
    '''
    print("SSIM: {}".format(score))
    cv2.imshow("1",thresh)
    cv2.imshow("2",orimg1)
    cv2.imshow("3",orimg2)
    cv2.waitKey(0)
    cv2.imwrite(os.path.join(path, "cap3.jpg"),item)
    '''
    item_list, loc_list = item_comp(before_item, current_item, img_list, orimg2)
    item_store(item_list, loc_list, path)
    return()


def item_store(itemList, positionList, directory):
    folder = directory + r'\item'
    storedItem = load_images_from_folder(folder)
    itemNum = len(storedItem)
    itemListNum = len(itemList)
    for i in range(itemListNum):
        flag = 0
        for j in range(itemNum):
            if item_match(itemList[i],storedItem[j]):
                frameStorage(directory,j,storedItem[j] , positionList[i], "u")
                flag =1
        if flag == 0:
            frameStorage(directory, itemNum,itemList[i], positionList[i], "i")
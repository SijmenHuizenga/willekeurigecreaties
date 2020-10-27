import cv2 as cv
import random
import numpy as np


def find_contours(img, thresh, minarea, maxarea):
    ret, thresh = cv.threshold(img, thresh, 255, 0)
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    out = []
    for contour in contours:
        if minarea < cv.contourArea(contour) < maxarea:
            out.append(contour)
    return out


def find_biggest_contours(img, minarea, maxarea):
    thresh = 100
    while True:
        contours = find_contours(img, thresh, minarea, maxarea)
        if len(contours) > 0:
            return contours
        thresh = thresh - 5
        if thresh < 20:
            return None


def process_image(filename, output_image, output_w, output_h):
    img = cv.imread(filename)
    if img is None or img.size == 0:
        return

    height = img.shape[0]
    width = img.shape[1]
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    contours = find_biggest_contours(imgray, (width*height)/10, (width*height)/4)
    if contours is None:
        return

    mask = np.zeros((height, width), np.uint8)
    cv.drawContours(mask, contours, -1, 10, cv.FILLED)
    # draw a semi-transparent outline
    cv.drawContours(mask, contours, -1, 5, 2)
    x, y, w, h = cv.boundingRect(mask)
    offset_x = random.randint(-1*x-100, output_w-w-x+100)
    offset_y = random.randint(-1*y-100, output_h-h-y+100)

    for row in range(height):
        for col in range(width):
            if mask[row][col] > 0:
                if row+offset_y >= output_h or col+offset_x >= output_w:
                    continue

                r, g, b = img[row][col]
                output_image[row+offset_y][col+offset_x] = (r, g, b, mask[row][col]/10)

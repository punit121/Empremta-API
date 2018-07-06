import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import sys
import json

# Path of working folder on Disk
#src_path = "E:/Lab/Python/Project/OCR/"
    



#img=sys.argv[1]
class MyEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)
        return json.dumps(data, cls=MyEncoder)

MIN_MATCH_COUNT = 10

def main(img):
    img1 = cv2.imread('test.png',0) # queryImage
    img2 = cv2.imread(img,0) # trainImage

    # OK
    # img1 = cv2.imread('nike_logo_invert_xs.png',0) # queryImage
    # img2 = cv2.imread('nike_athlete.png',0) # trainImage

    # Initiate SIFT detector
    sift1 = cv2.xfeatures2d.SIFT_create()
    sift2 = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift1.detectAndCompute(img1,None)
    kp2, des2 = sift2.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.8*n.distance:
            good.append(m)

    print(len(good))
    if(len(good)>=MIN_MATCH_COUNT):
        print("watermark detected")
        text_json = {'text' : "Yes" }
    else:
        text_json = {'text' : "No" }
    result= json.dumps(text_json, cls=MyEncoder)
    loaded_json = json.loads(result)

    print(loaded_json)
    f = open('data.txt', 'r+')
    f.truncate()
    with open('data.txt', 'w') as outfile:
        json.dump(loaded_json, outfile)

    return loaded_json

if __name__ == '__main__':

    url=sys.argv[1]
    main(url)

# OK

'''
if len(good)>=MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

else:
    print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

plt.imshow(img3, 'gray'),plt.show()
'''

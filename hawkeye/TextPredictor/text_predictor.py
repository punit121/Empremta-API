import cv2
import numpy as np
import pytesseract
import os
from PIL import Image
import sys
import json

# Path of working folder on Disk
#src_path = "E:/Lab/Python/Project/OCR/"
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


src_path = "TestImages"
def main(url):
    # Read image with opencv
    img = cv2.imread(url)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
     # Write image after removed noise
    cv2.imwrite("removed_noise.png", img)

    #  Apply threshold to get image with only black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite("thres.png", img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(url))

    # Remove template file
    #os.remove(temp)

    print("Start....")
    print(result)
    text_json = {'text' : result }
    result= json.dumps(text_json, cls=MyEncoder)
    loaded_json = json.loads(result)
    #for x in loaded_json:
    #  print("%s: %f" % (x, loaded_json[x]))
    print(loaded_json)
    f = open('data.txt', 'r+')
    f.truncate()
    with open('data.txt', 'w') as outfile:      
        json.dump(loaded_json, outfile) 

    return loaded_json  

if __name__ == '__main__':

    url=sys.argv[1]
    main(url)
    os.remove("removed_noise.png")
    os.remove("thres.png")   


#print('--- Start recognize text from image ---')
#print(get_string("TestImages/test2.jpeg")) 

#print("------ Done -------")   
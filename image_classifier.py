from edgetpu.classification.engine import ClassificationEngine
from PIL import Image

from gpio_rgb import LED

import cv2
import re
import os
import time

# the TFLite converted to be used with edgetpu
#modelPath = './model_edgetpu.tflite'

# The path to labels.txt that was downloaded with your model
#labelPath = './labels.txt'

class NoModelFile(Exception):
    pass

def searchFiles(dir_path, file_name):
    fileList = []
    res = ""

    for root, dirs, files in os.walk(dir_path):
        rootpath = os.path.join(os.path.abspath(dir_path), root)

        for file in files:
            filepath = os.path.join(rootpath, file)
            fileList.append(filepath)


    for s in fileList:
        #if "model_edgetpu.tflite" in s:
        if file_name in s:
            res = s
            break

    if res == "":
        raise NoModelFile

    return res



# This function parses the labels.txt and puts it in a python dictionary
def loadLabels(labelPath):
    p = re.compile(r'\s*(\d+)(.+)')
    with open(labelPath, 'r', encoding='utf-8') as labelFile:
        lines = (p.match(line).groups() for line in labelFile.readlines())
        return {int(num): text.strip() for num, text in lines}

# This function takes in a PIL Image from any source or path you choose
def classifyImage(image, engine):
    # Load and format your image for use with TM2 model
    # image is reformated to a square to match training
    #image = Image.open(image_path)
    #image.resize((224, 224))

    # Classify and ouptut inference
    classifications = engine.classify_with_image(image)
    print(classifications)

    if classifications[0][0] == 0 and classifications[0][1] > 0.95:
        class_num = LED.RED
    elif classifications[0][0] == 1 and classifications[0][1] > 0.95:
        class_num = LED.GREEN
    elif classifications[0][0] == 2 and classifications[0][1] > 0.95:
        class_num = LED.BLUE
    elif classifications[0][0] == 3 and classifications[0][1] > 0.95:
        class_num = LED.YELLOW
    elif classifications[0][0] == 4 and classifications[0][1] > 0.95:
        class_num = LED.PUPPLE
    elif classifications[0][0] == 5 and classifications[0][1] > 0.95:
        class_num = LED.LIGHT_BLUE
    elif classifications[0][0] == 6 and classifications[0][1] > 0.95:
        class_num = LED.WHITE
    else:
        class_num = -1

    return class_num

def main():

    '''
    modelPath = searchModelFile("/media")
    if not modelPath:
        print("No Model file")
		return
    '''
    try:
        modelFile = searchFiles("/media","model_edgetpu.tflite")
        labelFile = searchFiles("/media","labels.txt")
    except NoModelFile:
        print("No Model File Exception")
        return


    ledCont=LED()
    # Load yourf model onto your Coral Edgetpu
    labels = loadLabels(labelFile)

    if len(labels) < 1 or len(labels) > 6:
        print("Out of Bound")
        ledCont.setLedOn(LED.YELLOW)
        return

    engine = ClassificationEngine(modelFile)

    #initLED()
   # ledCont.wiggleLEDs(2)
    ledCont.startLEDs()

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Format the image into a PIL Image so its compatable with Edge TPU
        cv2_im = frame
        pil_im = Image.fromarray(cv2_im)

        # Resize and flip image so its a square and matches training
        pil_im.resize((224, 224))
        pil_im.transpose(Image.FLIP_LEFT_RIGHT)

        # Classify and display image
        results = classifyImage(pil_im, engine)
        #ledCont.setOnlyLED(results)
        if results >= 0: 
            ledCont.setLedOn(results)

        cv2.imshow('frame', cv2_im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()


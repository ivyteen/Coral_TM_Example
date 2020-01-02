from edgetpu.classification.engine import ClassificationEngine
from PIL import Image
import cv2
import re
import os
import time

import RPi.GPIO as rpigpio
LED_pins = [20, 13, 12, 25, 22]

# the TFLite converted to be used with edgetpu
#modelPath = './model_edgetpu.tflite'

# The path to labels.txt that was downloaded with your model
#labelPath = './labels.txt'

class NoModelFile(Exception):
    pass

def searchModelFile(path):
    fileList = []
    res = ""

    for root, dirs, files in os.walk(path):
        rootpath = os.path.join(os.path.abspath(path), root)

        for file in files:
            filepath = os.path.join(rootpath, file)
            fileList.append(filepath)


    for s in fileList:
        if "model_edgetpu.tflite" in s:
            res = s
            break

    if res == "":
        raise NoModelFile

    return res


def initLED():
    #Init for RPi GPIO for LED
    rpigpio.setmode(rpigpio.BCM)

    for pin in LED_pins:
        rpigpio.setwarnings(False)
        rpigpio.setup(pin, rpigpio.OUT)

def setLED(index, state):
    return rpigpio.output(LED_pins[index], rpigpio.LOW if state else rpigpio.HIGH)

def setOnlyLED(index):
    for i in range(len(LED_pins)): setLED(i, False)
    if index is not None: setLED(index, True)

def wiggleLEDs(reps=3):
    for i in range(reps):
        for i in range(5):
            setLED(i,True)
            time.sleep(0.05)
            setLED(i, False)


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
        class_num = 1
    elif classifications[0][0] == 1 and classifications[0][1] > 0.95:
        class_num = 2
    elif classifications[0][0] == 2 and classifications[0][1] > 0.95:
        class_num = 3
    elif classifications[0][0] == 3 and classifications[0][1] > 0.95:
        class_num = 4
    else:
        class_num = 0

    return class_num

def main():

    '''
    modelPath = searchModelFile("/media")
    if not modelPath:
        print("No Model file")
		return
    '''
    try:
        modelPath = searchModelFile("/media")
        # Load your model onto your Coral Edgetpu
        engine = ClassificationEngine(modelPath)
        #labels = loadLabels(labelPath)
    except NoModelFile:
        print("No Model File Exception")
        return

    initLED()
    wiggleLEDs(4)

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
        setOnlyLED(results)

        cv2.imshow('frame', cv2_im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


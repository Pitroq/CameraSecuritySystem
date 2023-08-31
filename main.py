import cv2
from datetime import datetime
import numpy as np
import time

def getDifference(frame1, frame2) :
    absDiff = cv2.absdiff(frame1, frame2)
    grayDiff = cv2.cvtColor(absDiff, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(grayDiff, 30, 255, cv2.THRESH_BINARY)
    
    nonZeroPixels = np.count_nonzero(threshold)
    totalPixels = threshold.shape[0] * threshold.shape[1]

    percentDifference = (nonZeroPixels / totalPixels) * 100
    return percentDifference

def isMotionDetected(frame1, frame2) :
    diff = getDifference(frame1, frame2)
    config = getConfig()
    if (diff > config["minPercentOfDifferenceToDetectMotion"]) :
        return True
    return False

def getConfig() :
    config = {}
    with open('config.cfg') as fp:
        for line in fp :
            if line.startswith('#'):
                continue
            key, val = line.strip().split('=')
            
            try :
                val = float(val)
            except:
                pass

            config[key] = val

    return config

def boolean(string):
    if string.lower() == "true":
        return True
    return False

def main():
    config = getConfig()
    cap = cv2.VideoCapture(int(config["cameraId"]))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = config["fps"]
    _, prevFrame = cap.read();

    recording = False
    noMotionFrames = 0;
    videoWriter = None
    isArmed = boolean(config["isArmed"])
    
    if isArmed:
        print("camera is armed")
    else:
        print("camera is unarmed")

    while True:
        config = getConfig()
        configIsArmed = boolean(config["isArmed"])
        if configIsArmed != isArmed :
            if isArmed :
                videoWriter.release()
                
            isArmed = configIsArmed
            if isArmed:
                print("camera is armed")
            else:
                print("camera is unarmed")

        if (not isArmed) :
            time.sleep(10)
            continue;

        _, frame= cap.read()
        isMotion = isMotionDetected(frame, prevFrame)

        if isMotion and not recording:
            print("motion detected!");
            recording = True
            filename = "video-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".mp4"
            videoWriter = cv2.VideoWriter("capturedVideos/" + filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
            videoWriter.write(prevFrame)

        if noMotionFrames >= fps * config["noMotionSecondsNumberToEndRecording"]: 
            recording = False;
            videoWriter.release()
            noMotionFrames = 0;

        if recording:
            if isMotion :
                noMotionFrames = 0
            else :
                noMotionFrames += 1

            videoWriter.write(frame)
            prevFrame = frame;

    cap.release()
    videoWriter.release()

if __name__ == "__main__" :
    main()


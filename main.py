import cv2
from datetime import datetime
import numpy as np

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
    # print(diff)
    if (diff > 0.14) :
        print(diff)
        return True
    return False

def main():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 10
    _, prevFrame = cap.read();

    recording = False
    noMotionFrames = 0;
    videoWriter = None
    while True:
        _, frame= cap.read()
        isMotion = isMotionDetected(frame, prevFrame)

        if isMotion == True and recording == False:
            print("motion detected!");
            recording = True
            filename = "video-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".mp4"
            videoWriter = cv2.VideoWriter("capturedVideos/" + filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
            videoWriter.write(prevFrame)

        if noMotionFrames >= fps * 5: 
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


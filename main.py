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
    if (diff > 0.1) :
        return True
    return False


def main():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 10

    filename = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    videoWriter = cv2.VideoWriter('basicvideo.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width,height))

    _, prevFrame = cap.read();

    while True:
        _, frame= cap.read()
        a = isMotionDetected(frame, prevFrame)
        print(a);


        videoWriter.write(frame)
        prevFrame = frame;

    cap.release()
    writer.release()


if __name__ == "__main__"  :
    main()


from human_tracking import *
from diff import *
path = r"C:\Users\13090\Desktop\testing"
createFolder(path)
tracking = human_tracking('com5', 9600, 1)
while True:
        human_tracking.begin_tracking(tracking, path)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == ord('q'):
            break



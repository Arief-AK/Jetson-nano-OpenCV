import cv2
print(cv2.__version__)

# Video ouput parameters
disp_width = 640
disp_height = 480
flip = 4

# Using 'G_streamer' that handles input video feed from the NVIDIA Jetson Nano
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(disp_width)+', height='+str(disp_height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

# Assign camera handle to video source (Waveshare webcam) using OpenCV instance
cam = cv2.VideoCapture(camSet)

while(True):
    feed_success_flag, frame=cam.read()
    cv2.imshow('Camera',frame)
    cv2.moveWindow('Camera',0,0)

    if(cv2.waitKey(1) == ord('q')):
        break

# Release memory
cam.release()
cv2.destroyAllWindows()

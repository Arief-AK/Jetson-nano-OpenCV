import cv2
print(cv2.__version__)

# Video ouput parameters
disp_width = 640
disp_height = 480
flip = 4

def none(x):
    pass

# Using 'G_streamer' that handles input video feed from the NVIDIA Jetson Nano
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(disp_width)+', height='+str(disp_height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

# Assign camera handle to video source (Waveshare webcam) using OpenCV instance
cam = cv2.VideoCapture(camSet)

# Create a window to handle some trackbars
cv2.namedWindow('Camera')
cv2.createTrackbar('x_value','Camera',10,disp_width,none)
cv2.createTrackbar('y_value','Camera',10,disp_height,none)
cv2.createTrackbar('width','Camera',50,150,none)
cv2.createTrackbar('height','Camera',50,150,none)

while(True):
    feed_success_flag, frame=cam.read()

    # Assign handles to the 'x' and 'y' axes of the trackbars
    track_handle_x = cv2.getTrackbarPos('x_value','Camera')
    track_handle_y = cv2.getTrackbarPos('y_value','Camera')

    # Assign handles to the 'width' and 'height' of the trackbars
    track_handle_width = cv2.getTrackbarPos('width','Camera')
    track_handle_height = cv2.getTrackbarPos('height','Camera')

    # Create a circle using the trackbars
    cv2.circle(frame,(track_handle_x,track_handle_y),5,(255,255,255),-1)
    cv2.rectangle(frame,(track_handle_x,track_handle_y),(track_handle_x+track_handle_width,track_handle_y+track_handle_height),(255,255,255),3)

    cv2.imshow('Camera',frame)
    cv2.moveWindow('Camera',0,0)

    if(cv2.waitKey(1) == ord('q')):
        break

# Release memory
cam.release()
cv2.destroyAllWindows()

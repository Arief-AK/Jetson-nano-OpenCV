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

# Initial loop
while(True):
    feed_success_flag, frame=cam.read() # Initialise the 'cam' object with respective parameters
    cv2.imshow('Camera',frame)          # Show frame using the window called 'Camera'
    cv2.moveWindow('Camera',0,0)        # Move the window to position (0,0)

    gray_window = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('Camera (Grayscale)',gray_window)
    cv2.moveWindow('Camera (Grayscale)',0,550)

    if(cv2.waitKey(1) == ord('q')):     # Wait for user input to quit
        break

# Release memory
cam.release()
cv2.destroyAllWindows()

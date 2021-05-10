# Imports

import cv2
import numpy as np

print(cv2.__version__)

# Globals
state = 0
current_event = -1
pixel_colours = [0,0,0]

# Video ouput parameters
disp_width = 640
disp_height = 480
flip = 4 

colour_image = np.zeros((250,250,3),np.uint8)

# This is a callback for the 'cv2 listener'. This handles any mouse events
def mouse_click(event,x_pos,y_pos,flags,params):

    global mouse_position
    global current_event

    if event == cv2.EVENT_LBUTTONDOWN:  # Event is 1
        
        mouse_position = (x_pos,y_pos)
        current_event = event

    if event == cv2.EVENT_RBUTTONDOWN:  # Event is 2
        
        mouse_position = (0,0)

        blue = frame[y_pos,x_pos,0]     # Get 'blue' value of the pixel at ROW 'y' COL 'x'. Colour format is BGR, therefore '0' is 'B' (Blue)
        green = frame[y_pos,x_pos,1]    # Get 'green' value of the pixel at ROW 'y' COL 'x'. Colour format is BGR, therefore '1' is 'B' (Green)
        red = frame[y_pos,x_pos,2]      # Get 'red' value of the pixel at ROW 'y' COL 'x'. Colour format is BGR, therefore '2' is 'B' (Red)
        
        pixel_colours[0] = blue
        pixel_colours[1] = green
        pixel_colours[2] = red

        current_event = event

def state_handle(state,event,frame):

    if(event != -1):

        if(event == 1):
            
            state = 1

            # Draw a small white circle
            cv2.circle(frame,mouse_position,5,(255,255,255),1)

        if(event == 2):

            state = 1

            #Print the colours of the pixel
            print('colours of the pixel (BGR)')
            print(pixel_colours[0],',',pixel_colours[1],',',pixel_colours[2])

            # Create a colour string
            colourString = str(pixel_colours[0])+','+str(pixel_colours[1])+','+str(pixel_colours[2])
            colour_image[:] = [pixel_colours[0],pixel_colours[1],pixel_colours[2]]

            # Add text onto the video output
            text_font   = cv2.FONT_HERSHEY_PLAIN
            new_red     = 255-int(pixel_colours[0])
            new_green   = 255-int(pixel_colours[1])
            new_blue    = 255-int(pixel_colours[2])
            new_spectrum = (new_blue,new_green,new_red)
            cv2.putText(colour_image,colourString,(10,25),text_font,1,new_spectrum,2)

            # Show the new window
            cv2.imshow('Colour grab',colour_image)

    else:
        state = 0

    return [state,frame]

# Window parameters
cv2.namedWindow('Camera')                       # Window name
cv2.setMouseCallback('Camera',mouse_click)      # Set mouse callback to listen for 'mouse_click'

# Using 'G_streamer' that handles input video feed from the NVIDIA Jetson Nano
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(disp_width)+', height='+str(disp_height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

# Assign camera handle to video source (Waveshare webcam) using OpenCV instance
cam = cv2.VideoCapture(camSet)

while(True):
    feed_success_flag, frame=cam.read()

    event_container = state_handle(state,current_event,frame)
    current_event = event_container[0]
    frame = event_container[1]

    cv2.imshow('Camera',frame)
    cv2.moveWindow('Camera',0,0)

    key_event = cv2.waitKey(1)

    if(key_event == ord('c')):
        current_event = -1

    if(key_event == ord('q')):
        break

# Release memory
cam.release()
cv2.destroyAllWindows()

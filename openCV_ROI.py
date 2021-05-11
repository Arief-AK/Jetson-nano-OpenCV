import cv2
print(cv2.__version__)

# Video ouput parameters
disp_width = 640
disp_height = 480
flip = 4

# Helper variables
rectangle_pos_x = 10
rectangle_pos_y = 10
incrementor_x = 5
incrementor_y = 5

def handle_collision(pos_x,pos_y,incrementor_x,incrementor_y):    
    if(pos_x < 10 or pos_x > 630):
        incrementor_x = -incrementor_x
    if((pos_x + 200 < 10) or (pos_x + 200 > 630)):
        incrementor_x = -incrementor_x
    if(pos_y < 10 or pos_y > 470):
        incrementor_y = -incrementor_y
    if((pos_y + 200) < 10 or (pos_y + 200) > 470):
        incrementor_y = -incrementor_y

    return [incrementor_x,incrementor_y]

# Using 'G_streamer' that handles input video feed from the NVIDIA Jetson Nano
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(disp_width)+', height='+str(disp_height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

# Assign camera handle to video source (Waveshare webcam) using OpenCV instance
cam = cv2.VideoCapture(camSet)

while(True):
    feed_success_flag, frame=cam.read()

    # Draw red rectangle
    frame=cv2.rectangle(frame,(rectangle_pos_x,rectangle_pos_y),(rectangle_pos_x+200,rectangle_pos_y+200),(0,0,255),2)

    # Update the position of the circle
    rectangle_pos_x = rectangle_pos_x + incrementor_x
    rectangle_pos_y = rectangle_pos_y + incrementor_y

    # Handle collision with walls if needed
    new_pos = handle_collision(rectangle_pos_x,rectangle_pos_y,incrementor_x,incrementor_y)

    #Update velocity vector
    incrementor_x = new_pos[0]
    incrementor_y = new_pos[1]    

    # Assign a Region Of Interest (ROI) using (ROW,COLUMN) coordinate format
    region_interest = frame[rectangle_pos_y:rectangle_pos_y+210,rectangle_pos_x:rectangle_pos_x+210].copy() # Create a copy of square region of 200px X 200px

    # Create the 'ROI' window and show it
    cv2.imshow('Region of Interest',region_interest)
    cv2.moveWindow('Region of Interest',705,0)

    # Covert 'frame' to gray-scale
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    cv2.imshow('Camera',frame)
    cv2.moveWindow('Camera',0,0)

    if(cv2.waitKey(1) == ord('q')):
        break

    """# Assign a Region Of Interest (ROI) using (ROW,COLUMN) coordinate format
    region_interest = frame[100:300,400:600].copy()                           # Create a copy of square region of 200px X 200px
    region_interest_gray = cv2.cvtColor(region_interest,cv2.COLOR_BGR2GRAY)         # Create a grayscale version of 'ROI'
    region_interest_gray = cv2.cvtColor(region_interest_gray,cv2.COLOR_GRAY2BGR)    # Create a copy of a the grayscale to display to 'frame'

    # Create the 'ROI' window and show it
    cv2.imshow('Region of Interest',region_interest)
    cv2.moveWindow('Region of Interest',705,0)

    # Create the 'ROI' (gray) window and show it
    cv2.imshow('Region of Interest (gray)',region_interest_gray)
    cv2.moveWindow('Region of Interest (gray)',705,250)

    # Hide the 'ROI' from main camera feed 'frame'
    frame[100:300,400:600] = [0,0,0]    
    frame[100:300,400:600] = region_interest_gray

    cv2.imshow('Camera',frame)
    cv2.moveWindow('Camera',0,0)

    if(cv2.waitKey(1) == ord('q')):
        break"""

# Release memory
cam.release()
cv2.destroyAllWindows()

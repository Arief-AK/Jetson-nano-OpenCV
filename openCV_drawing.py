import cv2
print(cv2.__version__)

# Video ouput parameters
disp_width = 640
disp_height = 480
flip = 4

# Helper variables
circ_pos_x = 10
circ_pos_y = 10
incrementor_x = 5
incrementor_y = 5

def handle_collision(pos_x,pos_y,incrementor_x,incrementor_y):    
    if(pos_x < 10 or pos_x > 630):
        incrementor_x = -incrementor_x
    if(pos_y < 10 or pos_y > 470):
        incrementor_y = -incrementor_y

    return [incrementor_x,incrementor_y]
    

# Using 'G_streamer' that handles input video feed from the NVIDIA Jetson Nano
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(disp_width)+', height='+str(disp_height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

# Assign camera handle to video source (Waveshare webcam) using OpenCV instance
cam = cv2.VideoCapture(camSet)

while(True):
    feed_success_flag, frame=cam.read()

    # Draw red circle
    frame=cv2.circle(frame,(circ_pos_x,circ_pos_y),25,(0,0,255),-1) 

    # Update the position of the circle
    circ_pos_x = circ_pos_x + incrementor_x
    circ_pos_y = circ_pos_y + incrementor_y

    # Handle collision with walls if needed
    new_pos = handle_collision(circ_pos_x,circ_pos_y,incrementor_x,incrementor_y)

    #Update velocity vector
    incrementor_x = new_pos[0]
    incrementor_y = new_pos[1]    

    """# Draw a red rectangle from the points (10,10) to (250,170) with line width of '7'
    frame=cv2.rectangle(frame,(10,10),(250,170),(0,0,255),7)

    # Draw a white circle in the middle of the frame
    frame=cv2.circle(frame,(320,240),50,(255,255,255),4)

    # Assign a font and display text onto the frame
    text_font = cv2.FONT_HERSHEY_DUPLEX
    frame=cv2.putText(frame,"Camera output",(200,320),text_font,1,(255,255,255),1)

    # Draw an arrow line
    frame=cv2.arrowedLine(frame,(10,320),(200,320),(0,0,0),2)"""

    cv2.imshow('Camera',frame)
    cv2.moveWindow('Camera',0,0)

    if(cv2.waitKey(1) == ord('q')):
        break

# Release memory
cam.release()
cv2.destroyAllWindows()

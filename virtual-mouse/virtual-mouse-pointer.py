# Import necessary libraries
import cv2
import mediapipe as mp
import pyautogui

# Open webcame and initialize hand detection
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize variables for thumb and index finger positions
index_y = 0

# Start loop for real-time processing
while True:
    # Read frame from webcam
    _, frame = cap.read()

    # Flip frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Get frame dimensions
    frame_height, frame_width, _ = frame.shape

    # Convert frame color from BGR to RGB and process with hand detector
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    # If any hand is detected
    if hands:
        # Loop through detected hands
        for hand in hands:
            # Draw landmarks on the frame
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            # Loop through each landmark in the hand
            for id, landmark in enumerate(landmarks):
                # Convert landmark coordinates to pixel values
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)

                # If it's the index fingertip
                if id == 8:
                    # Draw a circle at the fingertip position
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    # Convert to screen coordinates
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y
                
                # If it's the thumb tip
                if id == 4:
                    # Draw a circle at the thumb tip position
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    # Convert to screen coordinates
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y

                    # Debugging: print verticle distance between index finger and thumb
                    print('outside', abs(index_y - thumb_y))

                    # If index and thumb are close enough, perform click
                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1) # short pouse to prevent multiple clicks

                    # If fingers are fairly close, move the mouse pointer
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)

    # Show the frame with hand tracking
    cv2.imshow('Virtual Mouse', frame)

    # Wait for 1ms before next frame
    cv2.waitKey(1)
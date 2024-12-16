import os
import cv2

# Initialize the webcam (try different indexes if 0 doesn't work, e.g., 1, 2)
cap = cv2.VideoCapture(0)

# Check if the webcam is successfully opened
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Directory where images will be saved
directory = 'Image/'

# Ensure the base directory exists
os.makedirs(directory, exist_ok=True)

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Ensure directories exist for each letter
for letter in letters:
    os.makedirs(os.path.join(directory, letter), exist_ok=True)

# Main loop to capture frames and save images for each letter
print("Press corresponding keys to capture data for each letter. Press 'Esc' to quit.")

while True:
    # Read the frame from the webcam
    ret, frame = cap.read()
    
    # Check if frame is captured successfully
    if not ret:
        print("Error: Failed to grab frame")
        break

    # Draw the region of interest (ROI) on the frame
    cv2.rectangle(frame, (0, 40), (300, 400), (255, 255, 255), 2)
    cv2.imshow("Data", frame)  # Display the full frame
    cv2.imshow("ROI", frame[40:400, 0:300])  # Display the ROI

    # Extract the region of interest (ROI) for gesture detection
    roi_frame = frame[40:400, 0:300]

    # Capture key presses and save the corresponding image for each letter
    interrupt = cv2.waitKey(10)

    # Exit if 'Esc' (27 in ASCII) is pressed
    if interrupt == 27:  # Escape key to quit
        print("Exiting data collection.")
        break

    # Loop through letters to check key presses
    for letter in letters:
        if interrupt & 0xFF == ord(letter.lower()):  # Check if the key corresponds to the letter
            count = len(os.listdir(os.path.join(directory, letter)))  # Get count for the letter
            save_path = os.path.join(directory, letter, f"{count}.png")
            cv2.imwrite(save_path, roi_frame)
            print(f"Saved image for {letter}: {save_path}")  # Feedback
            break  # Exit the loop after capturing the image

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time
import os

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Create dataset directory
dataset_path = "dataset"
os.makedirs(dataset_path, exist_ok=True)

# User Input: Gesture Name
gesture_name = input("Enter gesture name: ").strip().lower()
csv_file = os.path.join(dataset_path, f"{gesture_name}.csv")

# Open Camera
cap = cv2.VideoCapture(0)

# Initialize data storage
data = []

print("📸 Press 'S' to save a sample, 'esc' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert frame to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Draw hand landmarks if detected
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
            data.append(landmarks)

    # Show frame
    cv2.imshow("Hand Gesture Collection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):  # Save Data
        if data:
            df = pd.DataFrame(data)
            df.to_csv(csv_file, index=False, mode='a', header=not os.path.exists(csv_file))
            print(f"✅ Saved {len(data)} samples for '{gesture_name}'.")
            data.clear()
    elif key == 27:  # Quit
        break

cap.release()
cv2.destroyAllWindows()
print("🚀 Data collection complete!")

import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, jsonify, Response
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)
 
 # Initialize MediaPipe Hand Model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
 
 # Open Webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
 
 # Function to Classify Gestures
def classify_gesture(landmarks):
    thumb_tip = np.array([landmarks[4].x, landmarks[4].y])
    index_tip = np.array([landmarks[8].x, landmarks[8].y])
    middle_tip = np.array([landmarks[12].x, landmarks[12].y])
    ring_tip = np.array([landmarks[16].x, landmarks[16].y])
    pinky_tip = np.array([landmarks[20].x, landmarks[20].y])
 
     # OK Gesture 👌 (Thumb & Index Touching)
    thumb_index_distance = np.linalg.norm(thumb_tip - index_tip)
    if thumb_index_distance < 0.05 and middle_tip[1] > index_tip[1]:
        return "Saranghaeyo 🫰"
 
     # Thumbs Up 👍 (Thumb Up, Fingers Folded)
    if thumb_tip[1] < index_tip[1] and all(landmarks[i].y > landmarks[i - 2].y for i in [8, 12, 16, 20]):
        return "Thumbs Up 👍"
 
     # Thumbs Down 👎 (Thumb Down, Fingers Folded)
    if thumb_tip[1] > index_tip[1] and all(landmarks[i].y > landmarks[i - 2].y for i in [8, 12, 16, 20]):
        return "Thumbs Down 👎"
 
     # Victory ✌️ (Index & Middle Finger Up, Others Down)
    if index_tip[1] < landmarks[6].y and middle_tip[1] < landmarks[10].y and \
        ring_tip[1] > landmarks[14].y and pinky_tip[1] > landmarks[18].y:
            return "Victory ✌️"
 
     # Open Palm 🖐️ (All Fingers Up)
    if all(landmarks[i].y < landmarks[i - 2].y for i in [8, 12, 16, 20]):
        return "Open Palm 🖐️"
 
     # Fist ✊ (All Fingers Folded)
    if all(landmarks[i].y > landmarks[i - 2].y for i in [8, 12, 16, 20]):
        return "Fist ✊"
 
     # Pointing Up ☝️ (Only Index Finger Up)
    if index_tip[1] < landmarks[6].y and all(landmarks[i].y > landmarks[i - 2].y for i in [12, 16, 20]):
        return "Pointing Up ☝️"
 
     # Pointing Left 👈 (Only Index Finger Extended Left)
    if index_tip[0] < thumb_tip[0] and all(landmarks[i].x > landmarks[i - 2].x for i in [12, 16, 20]):
        return "Pointing Left 👈"
 
     # Pointing Right 👉 (Only Index Finger Extended Right)
    if index_tip[0] > thumb_tip[0] and all(landmarks[i].x < landmarks[i - 2].x for i in [12, 16, 20]):
        return "Pointing Right 👉"
 
     # Rock Sign 🤘 (Index & Pinky Up, Others Down)
    if index_tip[1] < landmarks[6].y and pinky_tip[1] < landmarks[18].y and middle_tip[1] > landmarks[10].y and ring_tip[1] > landmarks[14].y:
        return "Rock 🤘"
 
     # Call Me Sign 🤙 (Thumb & Pinky Extended, Others Folded)
    if thumb_tip[0] < pinky_tip[0] and all(landmarks[i].y > landmarks[i - 2].y for i in [8, 12, 16]):
        return "Call Me 🤙"
 
     # Unknown Gesture
    return "Unknown Gesture"
 
 # Flask API to Provide Gesture Data
@app.route('/detect', methods=['GET'])
def detect_hand():
    ret, frame = cap.read()
    if not ret:
        return jsonify({"error": "Failed to capture frame"})
 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
 
    gesture = "Unknown"
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            gesture = classify_gesture(hand_landmarks.landmark)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
 
    return jsonify({"gesture": gesture})
 
 # Flask API to Provide Video Stream
@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
 
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)
 
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
 
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
 
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
 
if __name__ == "__main__":
    app.run(debug=True)

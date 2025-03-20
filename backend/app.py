import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, Response
from flask_cors import CORS

# Load Trained Model
model = tf.keras.models.load_model("hand_gesture_model.h5")

# Define Gesture Labels (Update based on your dataset)
gesture_labels = ["good_luck", "ok", "peace", "thank_you", "thumbs_up"]  

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Open Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

@app.route('/detect', methods=['GET'])
def detect_hand():
    """ Detects hand gestures and returns the predicted gesture. """
    ret, frame = cap.read()
    if not ret:
        return jsonify({"error": "Failed to capture frame"})

    # Convert frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks on frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract 21 landmark points (x, y, z) and flatten into a single array
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten().reshape(1, -1)

            # Predict Gesture
            prediction = model.predict(landmarks)
            gesture = gesture_labels[np.argmax(prediction)]

            # Display Gesture on Frame
            cv2.putText(frame, f"Gesture: {gesture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 0), 2, cv2.LINE_AA)

            return jsonify({"gesture": gesture})

    return jsonify({"gesture": "Unknown"})

@app.route('/video_feed')
def video_feed():
    """ Streams the live camera feed with hand landmarks. """
    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for MediaPipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            # Draw landmarks if hands are detected
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Convert frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Cleanup Function to Release Camera
with app.app_context():
    import atexit
    atexit.register(lambda: cap.release())


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

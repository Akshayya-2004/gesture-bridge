from flask import Flask, jsonify, Response
import cv2
import mediapipe as mp
import numpy as np
import atexit

app = Flask(__name__)

# Initialize Mediapipe Hand Module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

def classify_gesture(landmarks):
    """
    Classifies gestures based on hand landmark positions.
    """
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    # Rule-based classification
    if index_tip[1] < landmarks[6][1] and middle_tip[1] < landmarks[10][1]:
        return "Victory ✌️"
    elif index_tip[1] < landmarks[6][1] and middle_tip[1] > landmarks[10][1]:
        return "Index Finger Up ☝️"
    elif all(landmarks[i][1] > landmarks[i-2][1] for i in [8, 12, 16, 20]):
        return "Fist ✊"
    elif thumb_tip[0] > landmarks[2][0] and all(landmarks[i][1] > landmarks[6][1] for i in [8, 12, 16, 20]):
        return "Thumbs Up 👍"
    else:
        return "Unknown Gesture"
    
@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/detect', methods=['GET'])
def detect_hand():
    ret, frame = cap.read()
    if not ret:
        return jsonify({"error": "Failed to capture frame"})

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    landmarks_list = []
    gesture = "Unknown"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            landmarks = [(i, lm.x, lm.y, lm.z) for i, lm in enumerate(hand_landmarks.landmark)]
            gesture = classify_gesture(landmarks)  # Detect gesture
            landmarks_list.append(landmarks)

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Overlay gesture text
    cv2.putText(frame, f"Gesture: {gesture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2, cv2.LINE_AA)

    return jsonify({"gesture": gesture, "landmarks": landmarks_list})

def cleanup():
    cap.release()
    cv2.destroyAllWindows()

atexit.register(cleanup)


if __name__ == "__main__":
    app.run(debug=True)

hi

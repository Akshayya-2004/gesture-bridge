from flask import Flask, jsonify, Response
import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, Response
import atexit

app = Flask(__name__)

# Initialize Mediapipe Hand Module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

def classify_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    # VICTORY ✌️ (Index & Middle Finger Up, Others Down)
    if index_tip[1] < landmarks[6][1] and middle_tip[1] < landmarks[10][1] and \
       ring_tip[1] > landmarks[14][1] and pinky_tip[1] > landmarks[18][1]:
        return "Victory ✌️"

    # OPEN PALM 🖐️ (All Fingers Up)
    elif all(landmarks[i][1] < landmarks[i - 2][1] for i in [8, 12, 16, 20]):
        return "Open Palm 🖐️"

    # THUMBS UP 👍
    elif thumb_tip[0] > index_tip[0] and all(landmarks[i][1] > landmarks[6][1] for i in [8, 12, 16, 20]):
        return "Thumbs Up 👍"

    # FIST ✊ (All Fingers Down)
    elif all(landmarks[i][1] > landmarks[i - 2][1] for i in [8, 12, 16, 20]):
        return "Fist ✊"

    # OK 👌 (Thumb & Index Finger Form a Circle)
    elif abs(thumb_tip[0] - index_tip[0]) < 0.02 and abs(thumb_tip[1] - index_tip[1]) < 0.02:
        return "OK 👌"

    # UNKNOWN GESTURE
    else:
        return "Unknown Gesture"
    
@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert BGR to RGB for Mediapipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            # Draw landmarks if hands are detected
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
                    )

            # Convert frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

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



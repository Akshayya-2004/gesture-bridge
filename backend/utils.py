import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not detected!")
else:
    print("Camera is working.")

cap.release()
cv2.destroyAllWindows()

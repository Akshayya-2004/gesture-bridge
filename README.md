# GestureBridge - Sign Language Detector

GestureBridge is an AI-powered Sign Language Detection system developed to improve accessibility and communication for sign language users. The application uses computer vision and machine learning techniques to recognize hand gestures in real time through webcam input.

The project focuses on real-time gesture recognition, hand tracking, and AI-based interpretation using OpenCV and MediaPipe.

---

## Features

- Real-time sign language detection
- Hand tracking and gesture recognition
- Webcam-based live input processing
- AI-powered gesture interpretation
- Fast and responsive detection system
- Scalable backend architecture

---

## Tech Stack

### Frontend
- React.js

### Backend
- Python
- Flask

### AI / Computer Vision
- OpenCV
- MediaPipe

### Additional Libraries
- NumPy

---

## Project Structure

```bash
gesturebridge-sign-language-detector/
│
├── frontend/
│
├── backend/
│   ├── main.py
│   ├── asl_converter.py
│   ├── requirements.txt
│
└── README.md
```

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/your-username/gesturebridge-sign-language-detector.git
```

---

### Navigate to the project folder

```bash
cd gesturebridge-sign-language-detector
```

---

## Backend Setup

### Create a virtual environment

```bash
python -m venv venv
```

---

### Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

---

### Install dependencies

```bash
pip install -r backend/requirements.txt
```

---

### Run the backend server

```bash
python backend/main.py
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

## Screenshots

- Home page
<img width="369" height="265" alt="image" src="https://github.com/user-attachments/assets/0d204d73-e4e9-4190-8aca-647706707243" />

- Webcam gesture detection
<img width="383" height="261" alt="image" src="https://github.com/user-attachments/assets/f5fedea2-03e2-44e1-9adb-870c8eee017b" />

- Real-time sign recognition
<img width="373" height="275" alt="image" src="https://github.com/user-attachments/assets/e1415148-bfd7-4f43-a80b-7c3496569143" />

- Gesture output interface
<img width="376" height="278" alt="image" src="https://github.com/user-attachments/assets/01f9ce3b-d82c-4f87-8647-e2013e593c19" />

---

## Future Improvements

- Sentence-level gesture recognition
- Voice output support
- Multi-language support
- Improved gesture accuracy
- Mobile application support
- Real-time translation system

---

## Learning Outcomes

This project helped in understanding:
- Computer vision concepts
- Real-time hand tracking
- AI-based gesture recognition
- Flask backend integration
- React frontend development
- MediaPipe and OpenCV workflows

---

## Deployment

The project can be deployed using:
- Render
- Railway
- Vercel (Frontend)

---

## License

This project is created for learning and educational purposes.

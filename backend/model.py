import pandas as pd
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Load Dataset
dataset_path = "dataset"
gestures = os.listdir(dataset_path)
print("📂 Found Gestures:", gestures)

# Prepare Data
X, y = [], []
for label, gesture in enumerate(gestures):
    df = pd.read_csv(os.path.join(dataset_path, gesture))
    X.extend(df.values)
    y.extend([label] * len(df))

X = np.array(X)
y = np.array(y)

# Convert labels to categorical
y = tf.keras.utils.to_categorical(y, num_classes=len(gestures))

# Define Model
model = Sequential([
    Dense(128, activation='relu', input_shape=(X.shape[1],)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dense(len(gestures), activation='softmax')
])

# Compile Model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train Model
model.fit(X, y, epochs=20, batch_size=32, validation_split=0.2)

# Save Model
model.save("hand_gesture_model.h5")
print("🚀 Model training complete! Saved as 'hand_gesture_model.h5'.")

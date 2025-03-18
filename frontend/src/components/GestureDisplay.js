import React, { useState, useEffect } from "react";
import { getGesture } from "../api";

const GestureDisplay = () => {
    const [gesture, setGesture] = useState("Waiting for gesture...");
    const [gestureHistory, setGestureHistory] = useState([]);

    useEffect(() => {
        const interval = setInterval(async () => {
            const data = await getGesture();
            if (data?.gesture && data.gesture !== "Unknown") {
                setGesture(data.gesture);
                setGestureHistory(prevHistory => [data.gesture, ...prevHistory.slice(0, 4)]); // Show last 5 gestures
            }
        }, 500);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="text-center bg-gray-800 p-4 rounded-lg">
            <h2 className="text-xl font-bold">Detected Gesture</h2>
            <p className="text-2xl font-semibold mt-2">{gesture}</p>
            <h3 className="text-lg font-medium mt-4">Recent Gestures:</h3>
            <ul>
                {gestureHistory.map((g, index) => (
                    <li key={index} className="text-sm text-gray-400">{g}</li>
                ))}
            </ul>
        </div>
    );
};

export default GestureDisplay;

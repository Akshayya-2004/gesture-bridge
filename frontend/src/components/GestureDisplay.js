import React, { useState, useEffect } from "react";
import { getGesture } from "../api";

const GestureDisplay = () => {
    const [gesture, setGesture] = useState("Loading...");

    useEffect(() => {
        const interval = setInterval(async () => {
            const data = await getGesture();
            if (data?.gesture) {
                setGesture(data.gesture);
            }
        }, 500); // Faster updates

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="text-center bg-gray-800 p-4 rounded-lg">
            <h2 className="text-xl font-bold">Detected Gesture</h2>
            <p className="text-2xl font-semibold mt-2">{gesture}</p>
        </div>
    );
};

export default GestureDisplay;

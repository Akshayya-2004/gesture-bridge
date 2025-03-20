import React, { useEffect, useState } from "react";

const GestureDisplay = () => {
  const [gesture, setGesture] = useState("Loading...");

  useEffect(() => {
    const fetchGesture = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/detect"); // ✅ Fetch gesture data
        const data = await response.json();
        setGesture(data.gesture);
      } catch (error) {
        console.error("Error fetching gesture:", error);
        setGesture("Error detecting gesture");
      }
    };

    // Fetch gesture data every 4 seconds
    const interval = setInterval(fetchGesture, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <h1 className="text-3xl font-bold mb-4">Gesture Display</h1>

      {/* ✅ Display Live Camera Feed from Flask */}
      <div className="border-4 border-gray-700 rounded-lg overflow-hidden">
        <img
          src="http://127.0.0.1:5000/video_feed"
          alt="Live Camera Feed"
          className="w-96 h-72 object-cover"
        />
      </div>

      {/* ✅ Show detected gesture */}
      <p className="text-2xl bg-gray-800 px-6 py-3 rounded-lg shadow-lg mt-4">
        {gesture}
      </p>
    </div>
  );
};

export default GestureDisplay;

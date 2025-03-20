import React, { useState, useEffect } from "react";
 import { getGesture } from "../api";
 
 const GestureDisplay = () => {
     const [gesture, setGesture] = useState("Waiting for gesture...");
     const [gestureHistory, setGestureHistory] = useState([]);
 
     useEffect(() => {
         const interval = setInterval(async () => {
             const data = await getGesture();
             console.log("Received Gesture from API:", data);  // Debugging
 
             if (data?.gesture && data.gesture !== "Unknown") {
                 setGesture(data.gesture);
                 setGestureHistory(prevHistory => [data.gesture, ...prevHistory.slice(0, 4)]); // Keep last 5 gestures
             }
         }, 4000);  // Fetch every 4 seconds
 
         return () => clearInterval(interval);
     }, []);
 
     return (
         <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
             <h2 className="text-2xl font-semibold text-green-400">Detected Gesture</h2>
             <p className="text-3xl font-bold text-white mt-4 animate-pulse">{gesture}</p>
 
             <h3 className="text-lg font-medium mt-6 text-gray-400">Recent Gestures:</h3>
             <div className="flex justify-center mt-2 space-x-3">
                 {gestureHistory.map((g, index) => (
                     <span key={index} className="text-md bg-gray-700 px-3 py-1 rounded-full">
                         {g}
                     </span>
                 ))}
             </div>
         </div>
     );
 };
 
 export default GestureDisplay;
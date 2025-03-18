import React from "react";
import CameraFeed from "./components/CameraFeed";
import GestureDisplay from "./components/GestureDisplay";

const App = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-5">
            <h1 className="text-4xl font-bold mb-6 text-blue-400">🖐️ Sign Language Detector</h1>
            <div className="w-full max-w-4xl flex flex-col space-y-6">
                <div className="bg-gray-800 shadow-lg p-6 rounded-lg">
                    <CameraFeed />
                </div>
                <GestureDisplay />
            </div>
        </div>
    );
};

export default App;

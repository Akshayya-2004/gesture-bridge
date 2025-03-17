import React from "react";
import CameraFeed from "./components/CameraFeed";
import GestureDisplay from "./components/GestureDisplay";

const App = () => {
    return (
        <div className="flex flex-col items-center min-h-screen bg-gray-900 text-white p-5">
            <h1 className="text-3xl font-bold mb-4">Sign Language Detector 🖐️</h1>
            <div className="w-full max-w-3xl space-y-4">
                <CameraFeed />
                <GestureDisplay />
            </div>
        </div>
    );
};

export default App;

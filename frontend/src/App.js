import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import GestureLogin from "./GestureLogin";  // New login page
import SelectionPage from "./SelectionPage";  // New selection page
import CameraFeed from "./components/CameraFeed";  // Chat page
import GestureDisplay from "./components/GestureDisplay";  // Detection page

const App = () => {
    return (
        <Router>
            <Routes>
                {/* Gesture-based login is the first page */}
                <Route path="/" element={<GestureLogin />} />

                {/* Selection page after login */}
                <Route path="/select" element={<SelectionPage />} />

                {/* Chat page (previously rendered directly) */}
                <Route path="/chat" element={
                    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-5">
                        <h1 className="text-4xl font-bold mb-6 text-blue-400">🖐️ Sign Language Chat</h1>
                        <div className="w-full max-w-4xl flex flex-col space-y-6">
                            <div className="bg-gray-800 shadow-lg p-6 rounded-lg">
                                <CameraFeed />
                            </div>
                        </div>
                    </div>
                } />

                {/* Detection page */}
                <Route path="/detect" element={
                    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-5">
                        <h1 className="text-4xl font-bold mb-6 text-green-400">🔍 Sign Language Detection</h1>
                        <GestureDisplay />
                    </div>
                } />
            </Routes>
        </Router>
    );
};

export default App;

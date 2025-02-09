import React from "react";
import CameraFeed from "./components/CameraFeed";
import GestureDisplay from "./components/GestureDisplay";
import "./styles/App.css";

const App=()=>{
  return(
    <div className="app-container">
      <h1>Sign Language Detector</h1>
      <CameraFeed />
      <GestureDisplay />
    </div>
  );
};

export default App;

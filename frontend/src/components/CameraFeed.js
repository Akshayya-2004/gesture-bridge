import React from "react";

const CameraFeed = () => {
    return (
        <div className="relative w-full bg-black p-4 rounded-lg shadow-lg">
            <img 
                src="http://127.0.0.1:5000/video_feed" 
                alt="Camera Feed" 
                className="w-full rounded-lg border-2 border-blue-400"
            />
        </div>
    );
};

export default CameraFeed;

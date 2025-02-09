import React from "react";

const CameraFeed=()=>{
    return(
        <div>
            <h2>Live Camera Feed</h2>
            <img 
                src="http://127.0.0.1:5000/video_feed"
                alt="Camera Feed"
                style={{width: "100%",borderRadius:"10px"}}
            />
        </div>
    );
};

export default CameraFeed;
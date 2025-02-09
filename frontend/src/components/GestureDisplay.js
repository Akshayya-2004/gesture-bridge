import React, {useState,useEffect} from "react";
import {getGesture} from "../api/api";

const GestureDisplay=()=>{
    const [gesture,setGesture]=useState("Loading...");
    useEffect(()=>{
        const interval=setInterval(async()=>{
            const data=await getGesture();
            if(data?.gesture){
                setGesture(data.gesture);
            }
        },1000);
        return()=>clearInterval(interval);
    },[]);

    return(
        <div>
            <h2>Detected Gesture</h2>
            <p style={{fontSize:"1.5rem",fontWeight:"bold"}}>{gesture}</p>
        </div>
    );
};

export default GestureDisplay;
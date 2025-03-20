import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import * as handpose from "@tensorflow-models/handpose";
import * as tf from "@tensorflow/tfjs";
import Webcam from "react-webcam";
import { drawHand } from "../src/utils/drawHand";
import { Card } from "../src/components/ui/Card";
import { Loader } from "lucide-react";

const GestureLogin = () => {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const runHandpose = async () => {
      const net = await handpose.load();
      setLoading(false);

      setInterval(() => {
        detect(net);
      }, 100);
    };

    const detect = async (net) => {
      if (
        webcamRef.current &&
        webcamRef.current.video.readyState === 4
      ) {
        const video = webcamRef.current.video;
        const hand = await net.estimateHands(video);

        if (hand.length > 0) {
          const thumbTip = hand[0].landmarks[4];
          const indexTip = hand[0].landmarks[8];

          if (thumbTip[1] < indexTip[1]) {
            navigate("/select");
          }
        }

        const ctx = canvasRef.current.getContext("2d");
        drawHand(hand, ctx);
      }
    };

    runHandpose();
  }, [navigate]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
      <Card className="p-6 bg-gray-800 rounded-2xl shadow-lg flex flex-col items-center">
        <h1 className="text-xl font-bold mb-4">Sign in with a Thumbs-Up</h1>
        {loading && <Loader className="animate-spin" />}
        <Webcam ref={webcamRef} className="rounded-lg" />
        <canvas ref={canvasRef} className="absolute top-0 left-0" />
        <p className="mt-2 text-gray-400">Show a thumbs-up to login</p>
      </Card>
    </div>
  );
};

export default GestureLogin;

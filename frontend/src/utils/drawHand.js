export const drawHand = (hand, ctx) => {
    if (!hand || !ctx) return;

    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.fillStyle = "red";

    hand.forEach((prediction) => {
        const landmarks = prediction.landmarks;

        for (let i = 0; i < landmarks.length; i++) {
            const x = landmarks[i][0];
            const y = landmarks[i][1];
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI);
            ctx.fill();
        }
    });
};

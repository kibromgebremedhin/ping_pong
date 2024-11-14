const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const ws = new WebSocket("ws://localhost:6789");

let gameState = {};

ws.onmessage = function (event) {
    gameState = JSON.parse(event.data);
    drawGame();
};

function drawGame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw ball
    ctx.beginPath();
    ctx.arc(gameState.ball.x, gameState.ball.y, 8, 0, Math.PI * 2);
    ctx.fillStyle = "#FFF";
    ctx.fill();
    ctx.closePath();

    // Draw paddles
    ctx.fillStyle = "#FFF";
    ctx.fillRect(0, gameState.paddle1.y, 10, 60);
    ctx.fillRect(canvas.width - 10, gameState.paddle2.y, 10, 60);

    // Draw scores
    ctx.font = "20px Arial";
    ctx.fillText(gameState.score1, canvas.width / 4, 20);
    ctx.fillText(gameState.score2, (3 * canvas.width) / 4, 20);
}

document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowUp") ws.send(JSON.stringify({ paddle: 2, direction: -1 }));
    if (event.key === "ArrowDown") ws.send(JSON.stringify({ paddle: 2, direction: 1 }));
    if (event.key === "w") ws.send(JSON.stringify({ paddle: 1, direction: -1 }));
    if (event.key === "s") ws.send(JSON.stringify({ paddle: 1, direction: 1 }));
});

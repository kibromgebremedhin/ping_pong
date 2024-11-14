import asyncio
import websockets
import json
import random

WIDTH = 800
HEIGHT = 400
BALL_SPEED = 5
PADDLE_SPEED = 10
PADDLE_HEIGHT = 60
PADDLE_WIDTH = 10

class PongGame:
    def __init__(self):
        self.ball_x, self.ball_y = WIDTH // 2, HEIGHT // 2
        self.ball_dx, self.ball_dy = random.choice([-BALL_SPEED, BALL_SPEED]), random.choice([-BALL_SPEED, BALL_SPEED])
        self.paddle1_y, self.paddle2_y = HEIGHT // 2, HEIGHT // 2
        self.score1, self.score2 = 0, 0

    def move_ball(self):
        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Ball collision with top/bottom
        if self.ball_y <= 0 or self.ball_y >= HEIGHT:
            self.ball_dy = -self.ball_dy

        # Ball collision with paddles
        if (self.ball_x <= PADDLE_WIDTH and self.paddle1_y <= self.ball_y <= self.paddle1_y + PADDLE_HEIGHT) or \
           (self.ball_x >= WIDTH - PADDLE_WIDTH and self.paddle2_y <= self.ball_y <= self.paddle2_y + PADDLE_HEIGHT):
            self.ball_dx = -self.ball_dx

        # Check for scoring
        if self.ball_x <= 0:
            self.score2 += 1
            self.reset_ball()
        elif self.ball_x >= WIDTH:
            self.score1 += 1
            self.reset_ball()

    def reset_ball(self):
        self.ball_x, self.ball_y = WIDTH // 2, HEIGHT // 2
        self.ball_dx, self.ball_dy = random.choice([-BALL_SPEED, BALL_SPEED]), random.choice([-BALL_SPEED, BALL_SPEED])

    def move_paddle(self, paddle, direction):
        if paddle == 1:
            self.paddle1_y += direction * PADDLE_SPEED
            self.paddle1_y = max(0, min(self.paddle1_y, HEIGHT - PADDLE_HEIGHT))
        else:
            self.paddle2_y += direction * PADDLE_SPEED
            self.paddle2_y = max(0, min(self.paddle2_y, HEIGHT - PADDLE_HEIGHT))

    def get_state(self):
        return {
            "ball": {"x": self.ball_x, "y": self.ball_y},
            "paddle1": {"y": self.paddle1_y},
            "paddle2": {"y": self.paddle2_y},
            "score1": self.score1,
            "score2": self.score2
        }

# Define the game loop as an asynchronous function
async def game_loop(websocket, path):
    game = PongGame()
    while True:
        game.move_ball()
        await websocket.send(json.dumps(game.get_state()))
        await asyncio.sleep(0.05)

# Start the server with asyncio.run
async def main():
    async with websockets.serve(game_loop, "localhost", 6788):  # Changed port to 6788
        await asyncio.Future()  # Run forever

asyncio.run(main())

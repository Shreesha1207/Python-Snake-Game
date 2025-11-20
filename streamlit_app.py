import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Retro Snake", page_icon="🐍", layout="centered")

st.title("🐍 Retro Snake Game")
st.caption("Use your arrow keys to move. Press Space to start/restart.")

# HTML/CSS/JS Content
# I've modified the JS to use localStorage for high scores instead of the Flask API
game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retro Snake</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #2c3e50;
            --game-bg: #000;
            --snake-color: #2ecc71;
            --food-color: #e74c3c;
            --text-color: #ecf0f1;
            --accent-color: #f1c40f;
        }

        body {
            margin: 0;
            padding: 0;
            background-color: transparent; /* Transparent for Streamlit embedding */
            color: var(--text-color);
            font-family: 'Press Start 2P', cursive;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }

        .game-container {
            position: relative;
            padding: 20px;
            background: #34495e;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 4px solid #2c3e50;
        }

        .ui-panel {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding: 10px;
            background: #2c3e50;
            border-radius: 5px;
            border: 2px solid #1a252f;
        }

        .score-box {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .label {
            font-size: 10px;
            color: #95a5a6;
            margin-bottom: 5px;
        }

        #score, #high-score {
            font-size: 18px;
            color: var(--accent-color);
        }

        .title {
            font-size: 24px;
            color: var(--snake-color);
            text-shadow: 2px 2px 0px #000;
        }

        .canvas-wrapper {
            position: relative;
            border: 4px solid #95a5a6;
            border-radius: 4px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
            background-color: var(--game-bg);
        }

        canvas {
            display: block;
            background-color: var(--game-bg);
            /* CRT Scanline effect */
            background-image: linear-gradient(
                rgba(18, 16, 16, 0) 50%, 
                rgba(0, 0, 0, 0.25) 50%
            );
            background-size: 100% 4px;
        }

        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: rgba(0, 0, 0, 0.85);
            color: var(--text-color);
            text-align: center;
        }

        .hidden {
            display: none;
        }

        h1 {
            font-size: 40px;
            color: var(--snake-color);
            margin-bottom: 20px;
            text-shadow: 4px 4px 0px #000;
            animation: pulse 2s infinite;
        }

        p {
            font-size: 14px;
            line-height: 2;
            color: #fff;
        }

        .controls-hint {
            margin-top: 20px;
            text-align: center;
            font-size: 10px;
            color: #95a5a6;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="ui-panel">
            <div class="score-box">
                <span class="label">SCORE</span>
                <span id="score">0</span>
            </div>
            <div class="title">SNAKE</div>
            <div class="score-box">
                <span class="label">HI-SCORE</span>
                <span id="high-score">0</span>
            </div>
        </div>
        
        <div class="canvas-wrapper">
            <canvas id="gameCanvas" width="400" height="400"></canvas>
            <div id="start-screen" class="overlay">
                <h1>SNAKE</h1>
                <p>PRESS SPACE TO START</p>
            </div>
            <div id="game-over-screen" class="overlay hidden">
                <h1>GAME OVER</h1>
                <p>SCORE: <span id="final-score">0</span></p>
                <p>PRESS SPACE TO RESTART</p>
            </div>
        </div>
        
        <div class="controls-hint">
            USE ARROW KEYS TO MOVE
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const gridSize = 20;
        const tileCount = canvas.width / gridSize;

        let score = 0;
        // Load high score from localStorage
        let highScore = parseInt(localStorage.getItem('snakeHighScore')) || 0;
        document.getElementById('high-score').innerText = highScore;

        let snake = [
            { x: 10, y: 10 },
            { x: 9, y: 10 },
            { x: 8, y: 10 }
        ];
        let food = { x: 15, y: 15 };
        let dx = 0;
        let dy = 0;
        let nextDx = 0;
        let nextDy = 0;
        let gameRunning = false;
        let gameSpeed = 100;
        let lastRenderTime = 0;

        const startScreen = document.getElementById('start-screen');
        const gameOverScreen = document.getElementById('game-over-screen');
        const scoreElement = document.getElementById('score');
        const finalScoreElement = document.getElementById('final-score');
        const highScoreElement = document.getElementById('high-score');

        // Input handling
        // We need to focus the iframe for keys to work, so we add a click listener to the body
        document.body.addEventListener('click', () => {
            window.focus();
        });
        
        document.addEventListener('keydown', changeDirection);

        function changeDirection(event) {
            const LEFT_KEY = 37;
            const RIGHT_KEY = 39;
            const UP_KEY = 38;
            const DOWN_KEY = 40;
            const SPACE_KEY = 32;

            // Prevent default scrolling for arrow keys and space
            if([32, 37, 38, 39, 40].indexOf(event.keyCode) > -1) {
                event.preventDefault();
            }

            if (event.keyCode === SPACE_KEY) {
                if (!gameRunning) {
                    startGame();
                }
                return;
            }

            const keyPressed = event.keyCode;
            const goingUp = dy === -1;
            const goingDown = dy === 1;
            const goingRight = dx === 1;
            const goingLeft = dx === -1;

            if (keyPressed === LEFT_KEY && !goingRight) {
                nextDx = -1;
                nextDy = 0;
            }
            if (keyPressed === UP_KEY && !goingDown) {
                nextDx = 0;
                nextDy = -1;
            }
            if (keyPressed === RIGHT_KEY && !goingLeft) {
                nextDx = 1;
                nextDy = 0;
            }
            if (keyPressed === DOWN_KEY && !goingUp) {
                nextDx = 0;
                nextDy = 1;
            }
        }

        function startGame() {
            if (gameRunning) return;
            
            // Reset game state
            snake = [
                { x: 10, y: 10 },
                { x: 9, y: 10 },
                { x: 8, y: 10 }
            ];
            score = 0;
            dx = 1;
            dy = 0;
            nextDx = 1;
            nextDy = 0;
            scoreElement.innerText = score;
            gameRunning = true;
            
            startScreen.classList.add('hidden');
            gameOverScreen.classList.add('hidden');
            
            placeFood();
            requestAnimationFrame(gameLoop);
        }

        function gameLoop(currentTime) {
            if (!gameRunning) return;

            window.requestAnimationFrame(gameLoop);

            const secondsSinceLastRender = (currentTime - lastRenderTime) / 1000;
            if (secondsSinceLastRender < 1 / (1000 / gameSpeed)) return;

            lastRenderTime = currentTime;

            update();
            draw();
        }

        function update() {
            // Update direction
            dx = nextDx;
            dy = nextDy;

            // Move snake
            const head = { x: snake[0].x + dx, y: snake[0].y + dy };

            // Wall collision
            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                gameOver();
                return;
            }

            // Self collision
            for (let i = 0; i < snake.length; i++) {
                if (head.x === snake[i].x && head.y === snake[i].y) {
                    gameOver();
                    return;
                }
            }

            snake.unshift(head);

            // Eat food
            if (head.x === food.x && head.y === food.y) {
                score += 10;
                scoreElement.innerText = score;
                // Increase speed slightly
                if (gameSpeed > 50) gameSpeed -= 0.5;
                placeFood();
            } else {
                snake.pop();
            }
        }

        function draw() {
            // Clear canvas
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw food
            ctx.fillStyle = '#e74c3c';
            ctx.shadowBlur = 10;
            ctx.shadowColor = "#e74c3c";
            ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize - 2, gridSize - 2);
            ctx.shadowBlur = 0;

            // Draw snake
            snake.forEach((part, index) => {
                if (index === 0) {
                    ctx.fillStyle = '#2ecc71'; // Head
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = "#2ecc71";
                } else {
                    ctx.fillStyle = '#27ae60'; // Body
                    ctx.shadowBlur = 0;
                }
                ctx.fillRect(part.x * gridSize, part.y * gridSize, gridSize - 2, gridSize - 2);
            });
        }

        function placeFood() {
            food = {
                x: Math.floor(Math.random() * tileCount),
                y: Math.floor(Math.random() * tileCount)
            };
            // Check if food spawned on snake
            snake.forEach(part => {
                if (part.x === food.x && part.y === food.y) {
                    placeFood();
                }
            });
        }

        function gameOver() {
            gameRunning = false;
            finalScoreElement.innerText = score;
            gameOverScreen.classList.remove('hidden');
            
            if (score > highScore) {
                highScore = score;
                highScoreElement.innerText = highScore;
                localStorage.setItem('snakeHighScore', highScore);
            }
        }

        // Initial draw
        draw();
    </script>
</body>
</html>
"""

# Render the game in an iframe
components.html(game_html, height=600, scrolling=False)

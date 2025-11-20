const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const gridSize = 20;
const tileCount = canvas.width / gridSize;

let score = 0;
let highScore = parseInt(document.getElementById('high-score').innerText);

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
document.addEventListener('keydown', changeDirection);

function changeDirection(event) {
    const LEFT_KEY = 37;
    const RIGHT_KEY = 39;
    const UP_KEY = 38;
    const DOWN_KEY = 40;
    const SPACE_KEY = 32;

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
        saveHighScore(highScore);
    }
}

function saveHighScore(score) {
    fetch('/api/highscore', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ score: score }),
    })
        .then(response => response.json())
        .then(data => {
            console.log('High score saved:', data);
        })
        .catch((error) => {
            console.error('Error saving high score:', error);
        });
}

// Initial draw
draw();

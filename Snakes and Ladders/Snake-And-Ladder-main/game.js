const container = document.querySelector('.container');

for (let i = 100; i > 90; i--) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    cell.id = `cell-${i}`;
    cell.setAttribute('data-cell', i);  // ✅ Add this
    cell.innerText = i;
    container.appendChild(cell);
}

for (let i = 81; i < 91; i++) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    cell.id = `cell-${i}`;
    cell.setAttribute('data-cell', i);  // ✅ Add this
    cell.innerText = i;
    container.appendChild(cell);
}

for (let i = 80; i > 70; i--) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    cell.id = `cell-${i}`;
    cell.setAttribute('data-cell', i);  // ✅ Add this
    cell.innerText = i;
    container.appendChild(cell);
}

for (let i = 61; i <= 70; i++) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    cell.id = `cell-${i}`;
    cell.setAttribute('data-cell', i);  // ✅ Add this
    cell.innerText = i;
    container.appendChild(cell);
}

for (let i = 60; i > 50; i--) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    cell.id = `cell-${i}`;
    cell.setAttribute('data-cell', i);  // ✅ Add this
    cell.innerText = i;
    container.appendChild(cell);
}

for (let i = 41; i <= 50; i++) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    cell.id = `cell-${i}`;
    cell.setAttribute('data-cell', i);  // ✅ Add this
    cell.innerText = i;
    container.appendChild(cell);
}

for (let i = 40; i > 30; i--) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    cell.id = `cell-${i}`;
    cell.setAttribute('data-cell', i);  // ✅ Add this
    cell.innerText = i;
    container.appendChild(cell);
}

for (let i = 21; i <= 30; i++) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    cell.id = `cell-${i}`;
    cell.setAttribute('data-cell', i);  // ✅ Add this
    cell.innerText = i;
    container.appendChild(cell);
}

for (let i = 20; i > 10; i--) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    cell.id = `cell-${i}`;
    cell.setAttribute('data-cell', i);  // ✅ Add this
    cell.innerText = i;
    container.appendChild(cell);
}

for (let i = 1; i <= 10; i++) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    cell.id = `cell-${i}`;
    cell.setAttribute('data-cell', i);  // ✅ Add this
    cell.innerText = i;
    container.appendChild(cell);
}

// BOARD CREATED!!!

// colouring the cells

let eachCell = document.querySelectorAll('.cell');

for (box of eachCell) {
    let cell_num = box.innerText;
    if (cell_num % 2 === 0) {
        box.style.backgroundColor = " #7EBDC2";
    } else {
        box.style.backgroundColor = "#F3DFA2";
    }
}

const rollDice = () => Math.floor(Math.random() * 6) + 1;

// Snakes and ladders map
const snklad = {
    4: 25, 13: 25, 33: 49, 42: 63, 50: 69,
    62: 81, 74: 92, 97: 41, 89: 53, 76: 58,
    66: 45, 56: 31, 43: 18, 40: 3, 27: 5,
};

const snakes = [97, 89, 76, 66, 56, 43, 40, 27];
const snkend = [41, 53, 58, 45, 31, 18, 3, 5];
const ladders = [4, 13, 33, 42, 50, 62, 74];
const ladend = [25, 25, 49, 63, 69, 81, 92];
eachCell.forEach((cell) => {
    const cellNum = parseInt(cell.innerText);

    if (snakes.includes(cellNum)) {
        cell.style.backgroundColor = "#ff758f"; // red for snake start
        cell.innerHTML += " 🐍";
    }

    if (ladders.includes(cellNum)) {
        cell.style.backgroundColor = "#6BCB77"; // green for ladder start
        cell.innerHTML += " 🪜";
    }
});

// Check if current score hits a snake or ladder
const checkSnakeLadder = (score) => snklad[score] || score;

const buttonClick = document.querySelector('#roll-btn');
const userToken = document.querySelector('#user');
const compToken = document.querySelector('#comp');
const msgContainer = document.querySelector(".msg-container");
const msg = document.querySelector("#msg");
const diceValue = document.querySelector("#dice-value");

let userScore = 0;
let compScore = 0;
let userTurn = true;

// Move token on board
const moveToken = (token, position) => {
    const targetCell = document.querySelector(`#cell-${position}`);
    if (targetCell) {
        const cellRect = targetCell.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();

        const offsetTop = cellRect.top - containerRect.top + (cellRect.height / 2) - (token.offsetHeight / 2);
        const offsetLeft = cellRect.left - containerRect.left + (cellRect.width / 2) - (token.offsetWidth / 2);

        if (token.id === "user") {
            token.style.top = `${offsetTop - 5}px`;
            token.style.left = `${offsetLeft - 5}px`;
        } else {
            token.style.top = `${offsetTop + 5}px`;
            token.style.left = `${offsetLeft + 5}px`;
        }

    }
};

function drawStraightLine(fromCell, toCell, type) {
    const cell1 = document.querySelector(`[data-cell='${fromCell}']`);
    const cell2 = document.querySelector(`[data-cell='${toCell}']`);
    const svg = document.getElementById("board-overlay");

    const rect1 = cell1.getBoundingClientRect();
    const rect2 = cell2.getBoundingClientRect();
    const boardRect = svg.getBoundingClientRect();

    const x1 = rect1.left + rect1.width / 2 - boardRect.left;
    const y1 = rect1.top + rect1.height / 2 - boardRect.top;
    const x2 = rect2.left + rect2.width / 2 - boardRect.left;
    const y2 = rect2.top + rect2.height / 2 - boardRect.top;

    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", x1);
    line.setAttribute("y1", y1);
    line.setAttribute("x2", x2);
    line.setAttribute("y2", y2);
    line.setAttribute("class", "ladder-line");
    svg.appendChild(line);
}

function drawCurvedSnake(fromCell, toCell) {
    const cell1 = document.querySelector(`[data-cell='${fromCell}']`);
    const cell2 = document.querySelector(`[data-cell='${toCell}']`);
    const svg = document.getElementById("board-overlay");

    const rect1 = cell1.getBoundingClientRect();
    const rect2 = cell2.getBoundingClientRect();
    const boardRect = svg.getBoundingClientRect();

    const x1 = rect1.left + rect1.width / 2 - boardRect.left;
    const y1 = rect1.top + rect1.height / 2 - boardRect.top;
    const x2 = rect2.left + rect2.width / 2 - boardRect.left;
    const y2 = rect2.top + rect2.height / 2 - boardRect.top;

    const dx = x2 - x1;
    const dy = y2 - y1;
    const cx = x1 + dx / 2 - dy * 0.3;
    const cy = y1 + dy / 2 + dx * 0.3;

    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", `M ${x1},${y1} Q ${cx},${cy} ${x2},${y2}`);
    path.setAttribute("class", "snake-line");
    svg.appendChild(path);
}


// ✅ Draw images only after layout is complete
window.onload = () => {
    // Ladders: green
    for (let i = 0; i < ladders.length; i++) {
        drawStraightLine(ladders[i], ladend[i], "ladder");
    }

    // Snakes: red
    for (let i = 0; i < snakes.length; i++) {
        drawCurvedSnake(snakes[i], snkend[i]);
    }
};

// Check for winner
const checkWinner = () => {
    if (userScore === 100) return "User";
    if (compScore === 100) return "Computer";
    return false;
};

// Show winner banner
const showWinner = (winner) => {
    msg.innerText = `Congratulations, ${winner} wins!`;
    document.querySelector("#game-area").classList.add("hide");
    document.querySelector("#roll-btn").classList.add("hide");
    msgContainer.classList.remove("hide");
};


// Reset game
document.querySelector("#newGame").addEventListener("click", () => {
    userScore = 0;
    compScore = 0;
    userTurn = true;
    msgContainer.classList.add("hide");
    document.querySelector("#roll-btn").classList.remove("hide");
    document.querySelector("#game-area").classList.remove("hide");
    moveToken(userToken, 0);
    moveToken(compToken, 0);
    diceValue.innerText = "";
});



function updateDiceDisplay(isUser, rolls) {
    const player = isUser ? "You" : "Computer";
    const msg = `${player} rolled: ${rolls.join(', ')}`;
    document.getElementById("dice-value").innerText = msg;
}



// Game play function
const playGame = () => {
    if (userScore === 100 || compScore === 100 || !userTurn) return;

    let rollHistory = [];
    let totalMove = 0;
    let sixCount = 0;

    // USER TURN
    while (true) {
        let roll = rollDice();
        rollHistory.push(roll);

        if (roll === 6) {
            sixCount++;
            if (sixCount === 3) {
                totalMove = 0;
                rollHistory.push("→ 3 sixes! Move cancelled.");
                break;
            }
            totalMove += roll;
        } else {
            totalMove += roll;
            break;
        }
    }

    let tempScore = userScore + totalMove;
    if (tempScore <= 100) {
        userScore = checkSnakeLadder(tempScore);
    }
    moveToken(userToken, userScore);
    updateDiceDisplay(true, rollHistory);

    if (userScore === 100) {
        showWinner("User");
        return;
    }

    userTurn = false;

    // COMPUTER TURN (after delay)
    setTimeout(() => {
        if (userScore === 100) return;

        rollHistory = [];
        totalMove = 0;
        sixCount = 0;

        while (true) {
            let roll = rollDice();
            rollHistory.push(roll);

            if (roll === 6) {
                sixCount++;
                if (sixCount === 3) {
                    totalMove = 0;
                    rollHistory.push("→ 3 sixes! Move cancelled.");
                    break;
                }
                totalMove += roll;
            } else {
                totalMove += roll;
                break;
            }
        }

        let tempCompScore = compScore + totalMove;
        if (tempCompScore <= 100) {
            compScore = checkSnakeLadder(tempCompScore);
        }
        moveToken(compToken, compScore);
        updateDiceDisplay(false, rollHistory);

        if (compScore === 100) {
            showWinner("Computer");
            return;
        }

        userTurn = true;
    }, 1200);
};


buttonClick.addEventListener('click', playGame);




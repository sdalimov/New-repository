<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Математическая Игра</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
        button {
            padding: 10px 20px;
            font-size: 18px;
            cursor: pointer;
            background-color: #0088cc;
            color: white;
            border: none;
            border-radius: 5px;
        }
        #leaderboard {
            margin-top: 20px;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>Математическая Игра</h1>
    <button id="startButton">Начать игру</button>
    <h2>Таблица лидеров</h2>
    <ul id="leaderboard"></ul>
    
    <script>
        const levels = [
            { question: "2 + 2", answer: "4" },
            { question: "5 × 3", answer: "15" },
            { question: "12 ÷ 4", answer: "3" },
            // More levels can be added dynamically
        ];

        let currentLevel = 0;
        let score = 0;
        let attempts = 3; // Daily limit
        const SERVER_URL = "https://math-game-server.onrender.com";

        function startGame() {
            if (attempts <= 0) {
                alert("Вы использовали все попытки на сегодня!");
                return;
            }
            currentLevel = 0;
            score = 0;
            nextQuestion();
        }

        function nextQuestion() {
            if (currentLevel >= levels.length) {
                alert(`Поздравляем! Вы прошли все уровни! Итоговый счет: ${score}`);
                saveScore(score);
                return;
            }
            let userAnswer = prompt(levels[currentLevel].question);
            if (userAnswer === levels[currentLevel].answer) {
                score += 10;
                currentLevel++;
                nextQuestion();
            } else {
                alert(`Неверно! Игра окончена. Ваш счет: ${score}`);
                saveScore(score);
                attempts--;
            }
        }

        function saveScore(score) {
            const userName = prompt("Введите ваше имя для таблицы лидеров:");
            fetch(`${SERVER_URL}/submit-score`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: userName, score: score })
            })
            .then(response => response.json())
            .then(data => loadLeaderboard());
        }

        function loadLeaderboard() {
            fetch(`${SERVER_URL}/leaderboard`)
                .then(response => response.json())
                .then(data => {
                    const leaderboard = document.getElementById("leaderboard");
                    leaderboard.innerHTML = "";
                    data.forEach((player, index) => {
                        const li = document.createElement("li");
                        li.textContent = `${index + 1}. ${player.name} - ${player.score} очков`;
                        leaderboard.appendChild(li);
                    });
                });
        }

        window.onload = function () {
            document.getElementById("startButton").addEventListener("click", startGame);
            loadLeaderboard();
        };
    </script>
</body>
</html>

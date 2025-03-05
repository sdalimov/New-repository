const express = require("express");
const fs = require("fs");
const cors = require("cors");

const app = express();
const PORT = 3000;
const FILE_PATH = "leaderboard.json";

app.use(express.json());
app.use(cors());

// Загружаем таблицу лидеров
function loadLeaderboard() {
    if (!fs.existsSync(FILE_PATH)) {
        return [];
    }
    const data = fs.readFileSync(FILE_PATH);
    return JSON.parse(data);
}

// Сохраняем таблицу лидеров
function saveLeaderboard(leaderboard) {
    fs.writeFileSync(FILE_PATH, JSON.stringify(leaderboard, null, 2));
}

// Получение таблицы лидеров (ТОП-10)
app.get("/leaderboard", (req, res) => {
    const leaderboard = loadLeaderboard();
    leaderboard.sort((a, b) => b.score - a.score); // Сортировка по очкам
    res.json(leaderboard.slice(0, 10));
});

// Отправка нового результата
app.post("/submit-score", (req, res) => {
    const { name, score } = req.body;
    if (!name || typeof score !== "number") {
        return res.status(400).json({ message: "Неверные данные" });
    }
    const leaderboard = loadLeaderboard();
    leaderboard.push({ name, score });
    saveLeaderboard(leaderboard);
    res.json({ message: "Результат сохранен" });
});

// Запуск сервера
app.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
});

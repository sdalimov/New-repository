const express = require("express");
const fs = require("fs");
const cors = require("cors");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const FILE_PATH = path.join(__dirname, "leaderboard.json");

app.use(express.json());
app.use(cors());

// Загружаем таблицу лидеров
function loadLeaderboard() {
    if (!fs.existsSync(FILE_PATH)) {
        return [];
    }
    try {
        const data = fs.readFileSync(FILE_PATH, "utf-8");
        return JSON.parse(data);
    } catch (err) {
        console.error("Ошибка чтения файла:", err);
        return [];
    }
}

// Сохраняем таблицу лидеров
function saveLeaderboard(leaderboard) {
    try {
        fs.writeFileSync(FILE_PATH, JSON.stringify(leaderboard, null, 2), "utf-8");
    } catch (err) {
        console.error("Ошибка записи файла:", err);
    }
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

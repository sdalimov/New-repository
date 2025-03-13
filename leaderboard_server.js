const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

let db;

async function connectToMongo() {
    try {
        await client.connect();
        db = client.db('mathgame');
        console.log('Connected to MongoDB');
    } catch (error) {
        console.error('MongoDB connection error:', error);
    }
}

connectToMongo();

// Сохранение результата игры
app.post('/save-score', async (req, res) => {
    const { userName, score, userId } = req.body;
    if (!userName || typeof score !== 'number' || !userId) {
        return res.status(400).json({ message: 'Неверные данные' });
    }
    try {
        const user = await db.collection('users').findOneAndUpdate(
            { userId },
            { $set: { userName, score, updatedAt: new Date() }, $setOnInsert: { attempts: 3 } },
            { upsert: true, returnDocument: 'after' }
        );
        res.json({ success: true, user: user.value });
    } catch (error) {
        console.error('Error saving score:', error);
        res.status(500).json({ message: 'Ошибка сервера' });
    }
});

// Получение таблицы лидеров
app.get('/leaderboard', async (req, res) => {
    try {
        const leaderboard = await db.collection('users')
            .find()
            .sort({ score: -1 })
            .limit(10)
            .toArray();
        res.json(leaderboard);
    } catch (error) {
        console.error('Error fetching leaderboard:', error);
        res.status(500).json({ message: 'Ошибка сервера' });
    }
});

// Логика приглашения
app.post('/invite', async (req, res) => {
    const { inviterId } = req.body;
    if (!inviterId) {
        return res.status(400).json({ message: 'Не указан inviterId' });
    }
    try {
        // Сохраняем приглашение с временным уникальным кодом
        const inviteCode = Math.random().toString(36).substring(2, 10); // Генерируем случайный код
        await db.collection('invites').insertOne({
            inviterId,
            inviteCode,
            createdAt: new Date(),
            used: false
        });
        res.json({ success: true, inviteCode });
    } catch (error) {
        console.error('Error saving invite:', error);
        res.status(500).json({ message: 'Ошибка сервера' });
    }
});

// Проверка реферального бонуса
app.get('/check-referral', async (req, res) => {
    const { userId } = req.query;
    if (!userId) {
        return res.status(400).json({ message: 'Не указан userId' });
    }
    try {
        // Ищем, был ли этот userId приглашён
        const referral = await db.collection('invites').findOne({ used: false });
        if (referral && referral.inviterId !== userId) {
            // Проверяем, не приглашал ли пользователь сам себя
            const inviter = await db.collection('users').findOne({ userId: referral.inviterId });
            if (!inviter) {
                return res.json({ success: false, message: 'Пригласивший не найден' });
            }

            // Увеличиваем попытки пригласившего
            const updatedInviter = await db.collection('users').findOneAndUpdate(
                { userId: referral.inviterId },
                { $inc: { attempts: 1 } },
                { returnDocument: 'after' }
            );

            // Помечаем приглашение как использованное
            await db.collection('invites').updateOne(
                { inviteCode: referral.inviteCode },
                { $set: { used: true, usedBy: userId, usedAt: new Date() } }
            );

            res.json({ success: true, newAttempts: updatedInviter.value.attempts });
        } else {
            // Если нет подходящего приглашения, возвращаем текущие попытки пользователя
            const user = await db.collection('users').findOne({ userId });
            res.json({ success: false, newAttempts: user ? user.attempts : 3 });
        }
    } catch (error) {
        console.error('Error checking referral:', error);
        res.status(500).json({ message: 'Ошибка сервера' });
    }
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
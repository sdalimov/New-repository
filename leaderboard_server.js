const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/mathgame';

let db;

app.use(express.json());
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));

async function connectToMongo() {
    const client = new MongoClient(MONGO_URI);
    try {
        await client.connect();
        db = client.db('mathgame');
        console.log('Connected to MongoDB');
    } catch (error) {
        console.error('MongoDB connection error:', error);
    }
}

connectToMongo();

app.post('/save-score', async (req, res) => {
    const { userName, score, userId } = req.body;
    if (!userName || typeof score !== 'number') {
        return res.status(400).json({ message: 'Неверные данные' });
    }
    try {
        const user = await db.collection('users').findOneAndUpdate(
            { userId },
            { $set: { userName, score, updatedAt: new Date() } },
            { upsert: true, returnDocument: 'after' }
        );
        res.json({ success: true, user: user.value });
    } catch (error) {
        res.status(500).json({ message: 'Ошибка сервера' });
    }
});

app.get('/leaderboard', async (req, res) => {
    try {
        const leaderboard = await db.collection('users')
            .find()
            .sort({ score: -1 })
            .limit(10)
            .toArray();
        res.json(leaderboard.map(user => ({
            userName: user.userName,
            score: user.score
        })));
    } catch (error) {
        res.status(500).json({ message: 'Ошибка сервера' });
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on port ${PORT}`);
});
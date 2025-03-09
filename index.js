const express = require('express');
const { MongoClient } = require('mongodb');
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/mathgame';
let db;

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
    try {
        const user = await db.collection('users').findOneAndUpdate(
            { userId },
            { $set: { userName, score, updatedAt: new Date() } },
            { upsert: true, returnDocument: 'after' }
        );
        res.json({ success: true, user: user.value });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/invite', async (req, res) => {
    const { inviterId } = req.body;
    try {
        await db.collection('users').updateOne(
            { userId: inviterId },
            { $setOnInsert: { userName: 'Unknown', score: 0, attempts: 3 } },
            { upsert: true }
        );
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.get('/check-referral', async (req, res) => {
    const { userId } = req.query;
    try {
        const user = await db.collection('users').findOne({ userId });
        if (!user) {
            res.json({ success: false });
            return;
        }
        res.json({ success: true, newAttempts: user.attempts });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.get('/register', async (req, res) => {
    const { ref, userId } = req.query;
    try {
        const existingUser = await db.collection('users').findOne({ userId });
        if (!existingUser) {
            await db.collection('users').insertOne({
                userId,
                userName: 'Новый игрок',
                score: 0,
                attempts: 3,
                invitedBy: ref || null,
                createdAt: new Date()
            });
            if (ref) {
                const inviter = await db.collection('users').findOneAndUpdate(
                    { userId: ref },
                    { $inc: { attempts: 1 } },
                    { returnDocument: 'after' }
                );
                if (inviter) {
                    console.log(`User ${ref} invited ${userId}. Attempts increased to ${inviter.value.attempts}`);
                }
            }
        }
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
// backend/backend.js
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const dotenv = require("dotenv");
const mysql = require("mysql2");
const authRoutes = require("./routes/authRoutes");

dotenv.config();
const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static("../frontend")); // Serve frontend

// Connect to MySQL
const db = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
});

db.connect((err) => {
    if (err) {
        console.error("❌ MySQL Connection Error:", err);
    } else {
        console.log("✅ MySQL Connected");
    }
});

// Routes
app.use("/auth", authRoutes);

// Start Server
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:$({http://127.0.0.1:5500/FRONTED%20PAGE/index.html}`));
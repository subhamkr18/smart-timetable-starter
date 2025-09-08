// backend/routes/collegeConfig.js
import express from "express";
import fs from "fs";
import path from "path";

const router = express.Router();
const CONFIG_FILE = path.resolve("./backend/data/collegeConfig.json");

// ✅ GET saved config
router.get("/", (req, res) => {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      const data = JSON.parse(fs.readFileSync(CONFIG_FILE, "utf-8"));
      res.json(data);
    } else {
      res.json({});
    }
  } catch (err) {
    console.error("Error reading config:", err);
    res.status(500).json({ error: "Failed to read config" });
  }
});

// ✅ POST new config
router.post("/", (req, res) => {
  try {
    const config = req.body;

    // Ensure data folder exists
    const dir = path.dirname(CONFIG_FILE);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
    res.json({ message: "Config saved successfully" });
  } catch (err) {
    console.error("Error saving config:", err);
    res.status(500).json({ error: "Failed to save config" });
  }
});

export default router;

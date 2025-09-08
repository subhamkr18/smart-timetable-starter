// backend/server.js
import express from "express";
import bodyParser from "body-parser";
import cors from "cors";
import collegeConfigRoutes from "./routes/collegeConfig.js";

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Routes
app.use("/api/college-config", collegeConfigRoutes);

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});

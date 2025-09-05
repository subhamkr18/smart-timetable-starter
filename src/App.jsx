// App.jsx
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import FacultyDashboard from "./FacultyDashboard";

function Timetable() {
  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const periods = [
    { name: "Period 1", time: "9:00 - 9:50" },
    { name: "Period 2", time: "9:50 - 10:40" },
    { name: "Period 3", time: "10:40 - 11:30" },
    { name: "Period 4", time: "11:30 - 12:20" },
    { name: "Period 5", time: "12:20 - 1:10" },
    { name: "Lunch", time: "1:10 - 2:00", isLunch: true },
    { name: "Period 7", time: "2:00 - 2:50" },
    { name: "Period 8", time: "2:50 - 3:40" },
    { name: "Period 9", time: "3:40 - 4:30" },
  ];

  const [timetable] = useState({
    Monday: [
      { subject: "Math", teacher: "Dr. A", room: "101" },
      { subject: "Physics", teacher: "Dr. B", room: "102" },
      { subject: "Lab", teacher: "Dr. X", room: "Lab-1" },
      { subject: "Lab", teacher: "Dr. X", room: "Lab-1" },
      { subject: "English", teacher: "Dr. C", room: "103" },
      { isLunch: true },
      { subject: "Chemistry", teacher: "Dr. D", room: "104" },
      { subject: "Math", teacher: "Dr. A", room: "101" },
      { subject: "Sports", teacher: "Coach", room: "Ground" },
    ],
    Tuesday: [
      { subject: "English", teacher: "Dr. C", room: "103" },
      { subject: "Chemistry", teacher: "Dr. D", room: "104" },
      { subject: "Lab", teacher: "Dr. Y", room: "Lab-2" },
      { subject: "Lab", teacher: "Dr. Y", room: "Lab-2" },
      { subject: "Physics", teacher: "Dr. B", room: "102" },
      { isLunch: true },
      { subject: "Math", teacher: "Dr. A", room: "101" },
      { subject: "Elective", teacher: "Dr. E", room: "105" },
      { subject: "Workshop", teacher: "Dr. F", room: "Lab-3" },
    ],
    Wednesday: [{}, {}, {}, {}, {}, { isLunch: true }, {}, {}, {}],
    Thursday: [{}, {}, {}, {}, {}, { isLunch: true }, {}, {}, {}],
    Friday: [{}, {}, {}, {}, {}, { isLunch: true }, {}, {}, {}],
    Saturday: [{}, {}, {}, {}, {}, { isLunch: true }, {}, {}, {}],
  });

  return (
    <div className="app-container">
      <h1>📅 Smart Timetable</h1>
      <div className="table-wrapper">
        <table className="timetable">
          <thead>
            <tr>
              <th>Day</th>
              {periods.map((p, i) => (
                <th key={i}>
                  {p.isLunch ? "🍴 Lunch" : p.name}
                  <br />
                  <span className="time-text">{p.time}</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {days.map((day, dIndex) => (
              <tr key={dIndex}>
                <td className="day-cell">{day}</td>
                {timetable[day].map((period, pIndex) => {
                  const isLunch = period.isLunch;
                  const isLab = period.subject === "Lab";

                  return (
                    <td
                      key={pIndex}
                      className={
                        isLunch ? "lunch-cell" : isLab ? "lab-cell" : ""
                      }
                      title={
                        isLunch
                          ? "Lunch Break"
                          : period.subject
                          ? `Subject: ${period.subject}\nTeacher: ${period.teacher}\nRoom: ${period.room || "TBD"}`
                          : ""
                      }
                    >
                      {isLunch ? (
                        "🍴 Lunch"
                      ) : period.subject ? (
                        <>
                          <span className="subject-text">{period.subject}</span>
                          <span className="teacher-text">{period.teacher}</span>
                          <span className="room-text">
                            {period.room || "TBD"}
                          </span>
                        </>
                      ) : (
                        ""
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      {/* Top navigation links */}
      <nav className="top-nav">
        <Link to="/timetable">📅 Timetable</Link>
        <Link to="/dashboard">⚙️ Dashboard</Link>
      </nav>

      <Routes>
        <Route path="/" element={<h2>Welcome! Choose Timetable or Dashboard</h2>} />
        <Route path="/timetable" element={<Timetable />} />
        <Route path="/dashboard/*" element={<FacultyDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;

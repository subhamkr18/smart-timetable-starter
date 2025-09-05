import React from "react";
import { Link } from "react-router-dom";
import "./FacultyDashboard.css";

function FacultyDashboard() {
  return (
    <div className="faculty-dashboard">
      {/* Navbar */}
      <div className="navbar">
        {/* Left - Logo */}
        <div className="logo">Faculty Dashboard</div>

        {/* Center - Links */}
        <div className="nav-links">
          <Link to="/student" className="nav-item">Go to Student Dashboard</Link>
          <div className="nav-item">Courses</div>
          <div className="nav-item">Attendance</div>
          <div className="nav-item">Reports</div>
          <div className="nav-item">Communication</div>
        </div>

        {/* Right - Logout */}
        <button className="logout-btn">Logout</button>
      </div>

      {/* Content */}
      <div className="content">
        <h2>Welcome, Faculty 👩‍🏫</h2>
        <p>Here you can manage your courses, students, and communication.</p>
      </div>
    </div>
  );
}

export default FacultyDashboard;

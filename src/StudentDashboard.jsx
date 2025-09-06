import React, { useState } from "react";
import "./StudentDashboard.css";

function StudentDashboard() {
  const [activeDropdown, setActiveDropdown] = useState(null);

  const toggleDropdown = (id) => {
    setActiveDropdown(activeDropdown === id ? null : id);
  };

  return (
    <div className="dashboard">
      {/* Navbar */}
      <div className="navbar">
        <h1>Student Dashboard</h1>
        <div className="nav-links">
          <div className="nav-item" onClick={() => toggleDropdown("profile")}>
            Profile & Account
            {activeDropdown === "profile" && (
              <div className="dropdown">
                <div>View / Edit Profile</div>
                <div>Change Password</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("courses")}>
            Courses
            {activeDropdown === "courses" && (
              <div className="dropdown">
                <div>View Enrolled Courses</div>
                <div>Download Study Material</div>
                <div>Check Assignments</div>
                <div>Submit Assignment</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("attendance")}>
            Attendance
            {activeDropdown === "attendance" && (
              <div className="dropdown">
                <div>View Attendance</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("exam")}>
            Examination Section
            {activeDropdown === "exam" && (
              <div className="dropdown">
                <div>View Exam Schedule</div>
                <div>Download Admit Card</div>
                <div>Check Results</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("comm")}>
            Communication
            {activeDropdown === "comm" && (
              <div className="dropdown">
                <div>View Notices / Announcements</div>
                <div>Message Faculty</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("reports")}>
            Reports
            {activeDropdown === "reports" && (
              <div className="dropdown">
                <div>Performance Report</div>
              </div>
            )}
          </div>

          <div className="logout-btn">Logout</div>
        </div>
      </div>

      {/* Content */}
      <div className="content">
        {/* Welcome Section */}
        <div className="welcome">
          <h2>Welcome, Student</h2>
          <p>Here’s your academic overview and recent updates.</p>
        </div>

        {/* Stats Section */}
        <div className="stats">
          <div className="stat-card">
            <h2>5</h2>
            <p>Enrolled Courses</p>
          </div>
          <div className="stat-card">
            <h2>92%</h2>
            <p>Attendance</p>
          </div>
          <div className="stat-card">
            <h2>8</h2>
            <p>Assignments Pending</p>
          </div>
          <div className="stat-card">
            <h2>3</h2>
            <p>Upcoming Exams</p>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="recent">
          <h3>Recent Activity</h3>
          <ul>
            <li>Submitted Assignment 2 for DBMS (Today)</li>
            <li>New Notice: Internal Exam schedule (Yesterday)</li>
            <li>Attendance updated for CSE Batch (2 days ago)</li>
            <li>Result uploaded for OOPS (This week)</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default StudentDashboard;

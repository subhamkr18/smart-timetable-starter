import React, { useState } from "react";
import "./FacultyDashboard.css";

function FacultyDashboard() {
  const [activeDropdown, setActiveDropdown] = useState(null);

  const toggleDropdown = (id) => {
    setActiveDropdown(activeDropdown === id ? null : id);
  };

  return (
    <div className="dashboard">
      {/* Navbar */}
      <div className="navbar">
        <h1>Faculty Dashboard</h1>
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

          <div className="nav-item" onClick={() => toggleDropdown("classes")}>
            Classes
            {activeDropdown === "classes" && (
              <div className="dropdown">
                <div>View Assigned Classes</div>
                <div>Upload Study Material</div>
                <div>Check Assignments</div>
                <div>Grade Assignments</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("attendance")}>
            Attendance
            {activeDropdown === "attendance" && (
              <div className="dropdown">
                <div>Mark Attendance</div>
                <div>View Student Attendance</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("exam")}>
            Examination Section
            {activeDropdown === "exam" && (
              <div className="dropdown">
                <div>Upload Exam Schedule</div>
                <div>Upload Results</div>
                <div>Check Student Performance</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("comm")}>
            Communication
            {activeDropdown === "comm" && (
              <div className="dropdown">
                <div>Send Notices / Announcements</div>
                <div>Message Students</div>
                <div>Message Admin</div>
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
          <h2>Welcome, Faculty</h2>
          <p>Here’s your teaching overview and recent updates.</p>
        </div>

        {/* Stats Section */}
        <div className="stats">
          <div className="stat-card">
            <h2>4</h2>
            <p>Assigned Classes</p>
          </div>
          <div className="stat-card">
            <h2>150</h2>
            <p>Total Students</p>
          </div>
          <div className="stat-card">
            <h2>12</h2>
            <p>Assignments Pending Review</p>
          </div>
          <div className="stat-card">
            <h2>2</h2>
            <p>Exams to Conduct</p>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="recent">
          <h3>Recent Faculty Activity</h3>
          <ul>
            <li>Uploaded notes for DBMS (Today)</li>
            <li>Graded 10 assignments for OOPS (Yesterday)</li>
            <li>Attendance marked for CSE Batch (2 days ago)</li>
            <li>Shared exam guidelines with Admin (This week)</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default FacultyDashboard;

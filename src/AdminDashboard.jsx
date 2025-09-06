import React, { useState } from "react";
import "./AdminDashboard.css";

function AdminDashboard() {
  const [activeDropdown, setActiveDropdown] = useState(null);

  const toggleDropdown = (id) => {
    setActiveDropdown(activeDropdown === id ? null : id);
  };

  return (
    <div className="dashboard">
      {/* Navbar */}
      <div className="navbar">
        <h1>Admin Dashboard</h1>
        <div className="nav-links">
          <div className="nav-item" onClick={() => toggleDropdown("users")}>
            User Management
            {activeDropdown === "users" && (
              <div className="dropdown">
                <div>Add Faculty</div>
                <div>Add Student</div>
                <div>Manage Accounts</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("schedule")}>
            Scheduling
            {activeDropdown === "schedule" && (
              <div className="dropdown">
                <div>Create Timetable</div>
                <div>Manage Classrooms</div>
                <div>Allocate Faculty</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("exam")}>
            Exams
            {activeDropdown === "exam" && (
              <div className="dropdown">
                <div>Upload Exam Schedule</div>
                <div>Monitor Results</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("reports")}>
            Reports
            {activeDropdown === "reports" && (
              <div className="dropdown">
                <div>Attendance Reports</div>
                <div>Performance Reports</div>
              </div>
            )}
          </div>

          <div className="logout-btn">Logout</div>
        </div>
      </div>

      {/* Content */}
      <div className="content">
        {/* Welcome */}
        <div className="welcome">
          <h2>Welcome, Admin</h2>
          <p>Manage users, schedules, and reports from here.</p>
        </div>

        {/* Stats Section */}
        <div className="stats">
          <div className="stat-card">
            <h2>25</h2>
            <p>Total Faculty</p>
          </div>
          <div className="stat-card">
            <h2>320</h2>
            <p>Total Students</p>
          </div>
          <div className="stat-card">
            <h2>12</h2>
            <p>Active Classrooms</p>
          </div>
          <div className="stat-card">
            <h2>5</h2>
            <p>Pending Requests</p>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="recent">
          <h3>Recent Admin Actions</h3>
          <ul>
            <li>Added 3 new students (Today)</li>
            <li>Updated timetable for CSE Batch (Yesterday)</li>
            <li>Allocated new classroom for Physics (2 days ago)</li>
            <li>Reviewed faculty performance report (This week)</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;

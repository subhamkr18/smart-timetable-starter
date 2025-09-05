import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./AdminDashboard.css"; // create CSS file for styling

function AdminDashboard() {
  const [activeDropdown, setActiveDropdown] = useState(null);
  const navigate = useNavigate();

  const toggleDropdown = (id) => {
    setActiveDropdown(activeDropdown === id ? null : id);
  };

  return (
    <div className="admin-dashboard">
      {/* Navbar */}
      <div className="navbar">
        <h1>Admin Dashboard</h1>
        <div className="nav-links">
          <div className="nav-item" onClick={() => toggleDropdown("faculty")}>
            Manage Faculty
            {activeDropdown === "faculty" && (
              <div className="dropdown">
                <div>Add Faculty</div>
                <div>Update Faculty</div>
                <div>Remove Faculty</div>
                <Link to="/faculty"><div>Go to Faculty Dashboard</div></Link>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("students")}>
            Manage Students
            {activeDropdown === "students" && (
              <div className="dropdown">
                <div>Bulk Upload Students</div>
                <div>View Student List</div>
                <div>Approve/Deactivate Students</div>
                <Link to="/student"><div>Go to Student Dashboard</div></Link>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("academic")}>
            Academic Controls
            {activeDropdown === "academic" && (
              <div className="dropdown">
                <div>Manage Courses (Add/Update/Delete)</div>
                <div>Assign Courses to Faculty</div>
                <div>Class/Batch Management</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("exam")}>
            Examination & Results
            {activeDropdown === "exam" && (
              <div className="dropdown">
                <div>Create/Manage Exams</div>
                <div>Generate Reports</div>
                <div>Approve Results</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("comm")}>
            Communication
            {activeDropdown === "comm" && (
              <div className="dropdown">
                <div>Send Notice / Announcement</div>
                <div>Message Faculty or Students</div>
              </div>
            )}
          </div>

          <div className="nav-item" onClick={() => toggleDropdown("settings")}>
            Settings
            {activeDropdown === "settings" && (
              <div className="dropdown">
                <div>Change Admin Password</div>
                <div>College Information (Logo, Name, etc.)</div>
                <div>User Roles & Permissions</div>
              </div>
            )}
          </div>

          <div className="logout-btn" onClick={() => navigate("/")}>
            Logout
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="content">
        <h2>Welcome, Admin 👋</h2>
        <p>Select an option from the menu above to manage the portal.</p>
      </div>
    </div>
  );
}

export default AdminDashboard;

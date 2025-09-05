import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {
  const [role, setRole] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (!role) {
      alert("Please select a role first!");
      return;
    }
    if (role === "student") {
      navigate("/student");
    } else if (role === "faculty") {
      navigate("/faculty");
    } else if (role === "admin") {
      navigate("/admin");
    }
  };

  return (
    <div className="login-box">
      <h2>Login Portal</h2>

      <label htmlFor="role">Choose Role:</label>
      <select id="role" value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="">-- Select Role --</option>
        <option value="student">Student</option>
        <option value="faculty">Faculty</option>
        <option value="admin">Admin</option>
      </select>

      {/* Student Fields */}
      {role === "student" && (
        <div>
          <label htmlFor="regno">Registration Number:</label>
          <input type="text" id="regno" placeholder="Enter Registration No" />
          <label htmlFor="student-pass">Password:</label>
          <input type="password" id="student-pass" placeholder="Enter Password" />
        </div>
      )}

      {/* Faculty Fields */}
      {role === "faculty" && (
        <div>
          <label htmlFor="faculty-email">Email:</label>
          <input type="email" id="faculty-email" placeholder="Enter Faculty Email" />
          <label htmlFor="faculty-pass">Password:</label>
          <input type="password" id="faculty-pass" placeholder="Enter Password" />
        </div>
      )}

      {/* Admin Fields */}
      {role === "admin" && (
        <div>
          <label htmlFor="admin-user">Username:</label>
          <input type="text" id="admin-user" placeholder="Enter Username" />
          <label htmlFor="admin-pass">Password:</label>
          <input type="password" id="admin-pass" placeholder="Enter Password" />
        </div>
      )}

      <button type="button" onClick={handleLogin}>
        Login
      </button>
    </div>
  );
}

export default Login;

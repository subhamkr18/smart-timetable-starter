import React from "react";
import { useNavigate } from "react-router-dom";

function StudentDashboard() {
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <h1>Student Dashboard</h1>
      <p>Welcome, Student! Here’s your academic overview.</p>

      <button
        style={{ ...styles.button, background: "#e63946" }}
        onClick={() => navigate("/")}
      >
        Logout
      </button>
    </div>
  );
}

const styles = {
  container: {
    padding: "40px",
    textAlign: "center",
  },
  button: {
    marginTop: "20px",
    padding: "12px 20px",
    borderRadius: "8px",
    border: "none",
    background: "#17a2b8",
    color: "white",
    cursor: "pointer",
    fontSize: "16px",
  },
};

export default StudentDashboard;

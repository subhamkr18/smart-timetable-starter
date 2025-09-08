from backend.auth import get_password_hash

print("Admin:", get_password_hash("admin123"))
print("Faculty1:", get_password_hash("faculty123"))
print("Student1:", get_password_hash("student123"))

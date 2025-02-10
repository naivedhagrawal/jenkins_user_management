import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QTextEdit, QMessageBox
)

# Jenkins Configuration
JENKINS_URL = "http://your-jenkins-server.com"
ADMIN_USER = "admin"
API_TOKEN = "your_api_token"
AUTH = (ADMIN_USER, API_TOKEN)


class JenkinsManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # User Input Fields
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)

        self.fullname_label = QLabel("Full Name:")
        self.fullname_input = QLineEdit(self)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit(self)

        self.role_label = QLabel("Role Name:")
        self.role_input = QLineEdit(self)

        # Buttons
        self.create_user_btn = QPushButton("Create User", self)
        self.create_user_btn.clicked.connect(self.create_user)

        self.list_users_btn = QPushButton("List Users", self)
        self.list_users_btn.clicked.connect(self.list_users)

        self.assign_role_btn = QPushButton("Assign Role", self)
        self.assign_role_btn.clicked.connect(self.assign_role)

        self.delete_user_btn = QPushButton("Delete User", self)
        self.delete_user_btn.clicked.connect(self.delete_user)

        # Output Box
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)

        # Add widgets to layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.fullname_label)
        layout.addWidget(self.fullname_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.create_user_btn)
        layout.addWidget(self.list_users_btn)
        layout.addWidget(self.role_label)
        layout.addWidget(self.role_input)
        layout.addWidget(self.assign_role_btn)
        layout.addWidget(self.delete_user_btn)
        layout.addWidget(self.output_box)

        self.setLayout(layout)
        self.setWindowTitle("Jenkins User Manager")
        self.show()

    def create_user(self):
        """Creates a new user in Jenkins."""
        username = self.username_input.text()
        fullname = self.fullname_input.text()
        email = self.email_input.text()
        password = "password123"  # Default password for new users

        if not username or not fullname or not email:
            self.show_error("Please fill in all fields.")
            return

        url = f"{JENKINS_URL}/securityRealm/createAccountByAdmin"
        data = {
            "username": username,
            "password1": password,
            "password2": password,
            "fullname": fullname,
            "email": email,
        }
        response = requests.post(url, auth=AUTH, data=data)

        if response.status_code == 200:
            self.show_success(f"✅ User '{username}' created successfully.")
        else:
            self.show_error(f"❌ Failed to create user '{username}'.")

    def list_users(self):
        """Fetches and displays a list of users from Jenkins."""
        url = f"{JENKINS_URL}/asynchPeople/api/json"
        response = requests.get(url, auth=AUTH)

        if response.status_code == 200:
            users = response.json().get("users", [])
            user_list = "\n".join([user["id"] for user in users])
            self.output_box.setText(f"👥 Jenkins Users:\n{user_list}")
        else:
            self.show_error("❌ Failed to fetch user list.")

    def assign_role(self):
        """Assigns a role to a user."""
        username = self.username_input.text()
        role = self.role_input.text()

        if not username or not role:
            self.show_error("Please enter both username and role name.")
            return

        url = f"{JENKINS_URL}/role-strategy/strategy/assignRole"
        data = {
            "type": "globalRoles",
            "roleName": role,
            "sid": username,
        }
        response = requests.post(url, auth=AUTH, data=data)

        if response.status_code == 200:
            self.show_success(f"✅ Role '{role}' assigned to '{username}'.")
        else:
            self.show_error(f"❌ Failed to assign role '{role}' to '{username}'.")

    def delete_user(self):
        """Deletes a user from Jenkins."""
        username = self.username_input.text()

        if not username:
            self.show_error("Please enter a username to delete.")
            return

        url = f"{JENKINS_URL}/securityRealm/user/{username}/doDelete"
        response = requests.post(url, auth=AUTH)

        if response.status_code == 200:
            self.show_success(f"✅ User '{username}' deleted successfully.")
        else:
            self.show_error(f"❌ Failed to delete user '{username}'.")

    def show_success(self, message):
        """Displays a success message in the output box."""
        self.output_box.setText(message)

    def show_error(self, message):
        """Displays an error message in a popup."""
        QMessageBox.critical(self, "Error", message)


# Run the PyQt5 Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JenkinsManager()
    sys.exit(app.exec_())

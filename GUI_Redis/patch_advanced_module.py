from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QSizePolicy
import subprocess
from RedisCache_module import getRedis

class PatchManagementAdvancedModule(QWidget):
    def __init__(self, sudo_password):
        super(PatchManagementAdvancedModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()
        intro_label = QLabel(
            "Provides sophisticated tools for managing and deploying software patches, ensuring comprehensive system security.")
        intro_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)

        # Textbox for service
        self.service_textbox = QLineEdit(self)
        self.service_textbox.setPlaceholderText("Enter service name")
        layout.addWidget(self.service_textbox)

        # Button to prioritize updates
        prioritize_button = QPushButton('Prioritize Updates')
        prioritize_button.clicked.connect(self.run_prioritize_updates_script)
        layout.addWidget(prioritize_button)

        # Button to rollback updates
        reinstall_button = QPushButton('Reinstall Updates')
        reinstall_button.clicked.connect(self.run_reinstall_updates_script)
        layout.addWidget(reinstall_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"{getRedis(11)} '{command}'"
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"sudo bash -c {command}\n")
        process = subprocess.Popen(full_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Ensure sudo_password is a string
        sudo_password = str(self.sudo_password) + '\n'

        stdout, stderr = process.communicate(input=sudo_password)

        if process.returncode == 0:
            self.result_label.setText(stdout)
        else:
            self.result_label.setText(f"Error: {stderr}")

    def run_prioritize_updates_script(self):
        service_name = self.service_textbox.text()
        self.run_script(f"""
{getRedis(48)} {service_name}
{getRedis(49)}
{getRedis(1)} "Updates prioritized successfully."
""")

    def run_reinstall_updates_script(self):
        service_name = self.service_textbox.text()
        self.run_script(f"""
{getRedis(50)} {service_name}
{getRedis(1)} "Rollback complete for specified service."
""")

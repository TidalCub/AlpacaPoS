import sys
import paho.mqtt.client as mqtt
from PyQt6.QtWidgets import (
    QApplication, QStackedWidget, QWidget, QVBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QMessageBox, QProgressBar
)
from config_manager import Config_Manager

class SetupWizard(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Step 1: Enter MQTT Details
        self.step1 = QWidget()
        self.setup_step1()

        # Step 2: Test MQTT Connection
        self.step2 = QWidget()
        self.setup_step2()

        # Step 3: Select Device Type
        self.step3 = QWidget()
        self.setup_step3()

        self.addWidget(self.config)
        self.addWidget(self.step2)
        self.addWidget(self.step3)

        self.setWindowTitle("Setup Wizard")
        self.resize(400, 250)

    def setup_step1(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Step 1: Enter MQTT Details"))

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Enter MQTT Host")
        layout.addWidget(self.host_input)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Enter MQTT Port (Default: 1883)")
        layout.addWidget(self.port_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter MQTT Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter MQTT Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.go_to_step2)
        layout.addWidget(next_button)

        self.step1.setLayout(layout)

    def go_to_step2(self):
        self.host = self.host_input.text()
        self.port = self.port_input.text() or "1883"
        self.username = self.username_input.text() or ""
        self.password = self.password_input.text() or ""
        self.status_label.setText("Saving Config")

        config = {
            "authentication": {
                "username": self.username,
                "password": self.password
            },
            "MQTT_BROKER": {
                "host": self.host,
                "port": self.port
            }
        }

        Config_Manager().create_config(config)
        Config_Manager().encrypt()
        
        if not self.host:
            QMessageBox.critical(self, "Error", "Please enter a valid MQTT Host")
            return

        self.setCurrentWidget(self.step2)
        self.test_mqtt_connection()

    def setup_step2(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Step 2: Testing MQTT Connection..."))

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.next_button2 = QPushButton("Next")
        self.next_button2.setEnabled(False)
        self.next_button2.clicked.connect(lambda: self.setCurrentWidget(self.step3))
        layout.addWidget(self.next_button2)

        self.step2.setLayout(layout)

    def test_mqtt_connection(self):
        self.progress_bar.setValue(50)
        self.status_label.setText("Connecting...")

        client = mqtt.Client()
        client.username_pw_set(self.username, self.password)
        try:
            client.connect(self.host, int(self.port), 60)
            client.loop_start()
            self.status_label.setText("Connection Successful!")
            self.progress_bar.setValue(100)
            self.next_button2.setEnabled(True)
        except Exception as e:
            self.status_label.setText(f"Connection Failed: {e}")
            self.progress_bar.setValue(0)

    def setup_step3(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Step 3: Select Device Type"))

        self.device_select = QComboBox()
        self.device_select.addItems(["Printer", "POS Terminal", "Order Screen", "Kitchen Display", "Kiosk"])
        layout.addWidget(self.device_select)

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.go_to_step4)
        layout.addWidget(next_button)

        self.step3.setLayout(layout)

    def go_to_step4(self):
        self.device_type = self.device_select.currentText()
        self.setCurrentWidget(self.step4)
      
if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = SetupWizard()
    wizard.show()
    sys.exit(app.exec())

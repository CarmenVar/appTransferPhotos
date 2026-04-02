from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, correct_password):
        super().__init__()
        self.correct_password = correct_password
        self.setWindowTitle("Access Required")
        self.setMinimumSize(450, 300)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setObjectName("LoginDialog")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("☁ CloudTransfer")
        title.setObjectName("LoginTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Please enter your access password")
        subtitle.setObjectName("LoginSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        self.password_input = QLineEdit()
        self.password_input.setObjectName("PasswordInput")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.returnPressed.connect(self.check_password)
        layout.addWidget(self.password_input)
        
        self.error_label = QLabel("")
        self.error_label.setObjectName("ErrorLabel")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)
        
        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Unlock")
        self.login_btn.setObjectName("LoginBtn")
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.clicked.connect(self.check_password)
        btn_layout.addWidget(self.login_btn)
        
        layout.addLayout(btn_layout)
        
    def check_password(self):
        if self.password_input.text() == self.correct_password:
            self.accept()
        else:
            self.error_label.setText("Invalid password. Please try again.")
            self.password_input.clear()

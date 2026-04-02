import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Set the working directory to the script's directory so relative paths work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Load stylesheet
    try:
        with open("ui/style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: ui/style.qss not found. Running without custom stylesheet.")
        
    from ui.login_dialog import LoginDialog
    login = LoginDialog("carloscloud2026")
    if login.exec() != LoginDialog.DialogCode.Accepted:
        sys.exit(0)
        
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

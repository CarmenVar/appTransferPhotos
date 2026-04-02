from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cloud Photo Transfer Tool")
        self.resize(1000, 700)
        
        self.setObjectName("MainWindow")
        
        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Sidebar
        from .sidebar import Sidebar
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)
        
        # Main Panel
        from .main_panel import MainPanel
        self.main_panel = MainPanel()
        self.main_layout.addWidget(self.main_panel)

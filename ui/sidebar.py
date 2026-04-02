from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(240)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(20)
        
        # App Title / Brand
        title_label = QLabel("☁ CloudTransfer")
        title_label.setObjectName("AppTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(title_label)
        
        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        # Navigation items
        nav_label1 = QLabel("◓ Dashboard")
        nav_label1.setObjectName("NavItemActive")
        
        layout.addWidget(nav_label1)
        
        # Spacer to push storage down
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Storage Section
        storage_container = QWidget()
        storage_container.setObjectName("StorageContainer")
        storage_layout = QVBoxLayout(storage_container)
        storage_layout.setContentsMargins(20, 20, 20, 20)
        storage_layout.setSpacing(10)
        
        storage_title = QLabel("☁ GCS Storage")
        storage_title.setObjectName("StorageTitle")
        
        storage_bar = QProgressBar()
        storage_bar.setObjectName("StorageBar")
        storage_bar.setValue(60) # 60% Used as per request
        storage_bar.setTextVisible(False)
        storage_bar.setFixedHeight(6)
        
        storage_val = QLabel("60 GB Used / 100 GB")
        storage_val.setObjectName("StorageValue")
        
        storage_layout.addWidget(storage_title)
        storage_layout.addWidget(storage_bar)
        storage_layout.addWidget(storage_val)
        
        layout.addWidget(storage_container)

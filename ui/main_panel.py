from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QProgressBar, QListWidget, QListWidgetItem,
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QLineEdit, QMessageBox

import os
import glob
from logic.gcs_downloader import GCSDownloader

class MainPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainPanel")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Recent Downloads")
        title.setObjectName("PanelTitle")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Grid/List for Photos
        self.photo_list = QListWidget()
        self.photo_list.setObjectName("PhotoGrid")
        self.photo_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.photo_list.setIconSize(QSize(200, 150))
        self.photo_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.photo_list.setSpacing(15)
        self.photo_list.setMovement(QListWidget.Movement.Static)
        
        layout.addWidget(self.photo_list)
        
        # Bottom Layout: Progress Bar + Button
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(30)
        
        # Progress Bar section
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(8)
        progress_label = QLabel("Downloading 24 of 89 photos... (65%)")
        progress_label.setObjectName("ProgressLabel")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("MainProgressBar")
        self.progress_bar.setValue(65)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        
        # Progress labels
        self.stats_layout = QHBoxLayout()
        self.files_label = QLabel("Files: 0 / 0")
        self.time_label = QLabel("Elapsed: 00:00")
        self.eta_label = QLabel("ETA: --:--")
        
        self.stats_layout.addWidget(self.files_label)
        self.stats_layout.addStretch()
        self.stats_layout.addWidget(self.time_label)
        self.stats_layout.addStretch()
        self.stats_layout.addWidget(self.eta_label)
        
        progress_layout.addLayout(self.stats_layout)
        progress_layout.addWidget(self.progress_bar)
        
        bottom_layout.addLayout(progress_layout)
        bottom_layout.setStretchFactor(progress_layout, 1)
        
        # Button Menu
        btn_layout_final = QVBoxLayout()
        
        self.download_btn = QPushButton("Download All")
        self.download_btn.setObjectName("DownloadBtn")
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.setFixedSize(160, 50)
        self.download_btn.setEnabled(True) 
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("CancelBtn")
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setFixedSize(100, 50)
        self.cancel_btn.hide() # Hidden initially
        
        btn_layout_final.addWidget(self.download_btn)
        btn_layout_final.addWidget(self.cancel_btn)
        
        self.cancel_btn.clicked.connect(self.cancel_download)
        
        # Glow Effect via DropShadow
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(25)
        glow.setColor(QColor(74, 144, 226, 150))
        glow.setOffset(0, 0)
        self.download_btn.setGraphicsEffect(glow)
        
        bottom_layout.addLayout(btn_layout_final)
        
        layout.addLayout(bottom_layout)
        
        # Load mocks if available (we keep UI look)
        self.load_mock_photos()
        
        # Wire up button
        self.download_btn.clicked.connect(self.start_download)
        
        # Downloader reference
        self.downloader = None
        self.expected_token = os.environ.get("TRANSFER_APP_TOKEN", "secure-token-123")

    def start_download(self):
        # Confirmation Reassurance
        reply = QMessageBox.question(self, "Confirm Download", 
                                    "You are about to download approx. 60GB of photos.\n"
                                    "Please ensure you have enough disk space.\n\n"
                                    "Do you want to continue?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.No:
            return

        self.download_btn.setEnabled(False)
        self.cancel_btn.show()
        self.download_btn.setText("Downloading...")
        
        # Reset labels
        self.files_label.setText("Starting...")
        
        bucket_name = "calin-fotos-2026"
        target_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'downloads'))
        
        self.downloader = GCSDownloader(bucket_name, target_dir)
        self.downloader.progress_updated.connect(self.update_progress)
        self.downloader.download_finished.connect(self.download_complete)
        self.downloader.download_cancelled.connect(self.download_cancelled)
        self.downloader.error_occurred.connect(self.show_error)
        self.downloader.start()

    def cancel_download(self):
        if self.downloader:
            self.downloader.stop()
            self.cancel_btn.setEnabled(False)
            self.cancel_btn.setText("Stopping...")

    def update_progress(self, current_bytes, total_bytes, current_file, current_count, total_count, speed):
        # Update progress bar
        if total_bytes > 0:
            pct = int((current_bytes / total_bytes) * 100)
            self.progress_bar.setValue(pct)
            
        self.files_label.setText(f"Files: {current_count} / {total_count}")
        
        # Time calc
        import time
        elapsed = time.time() - self.downloader.start_time
        self.time_label.setText(f"Elapsed: {int(elapsed//60):02d}:{int(elapsed%60):02d}")
        
        if speed > 0:
            remaining_bytes = total_bytes - current_bytes
            eta_secs = remaining_bytes / speed
            self.eta_label.setText(f"ETA: {int(eta_secs//60):02d}:{int(eta_secs%60):02d}")

    def download_cancelled(self):
        self.cancel_btn.hide()
        self.cancel_btn.setEnabled(True)
        self.cancel_btn.setText("Cancel")
        self.download_btn.setEnabled(True)
        self.download_btn.setText("Download All")
        QMessageBox.information(self, "Cancelled", "The download was cancelled.")

    def download_complete(self, count):
        self.cancel_btn.hide()
        self.download_btn.setEnabled(True)
        self.download_btn.setText("Download All")
        self.files_label.setText(f"Completed! {count} files")
        self.progress_bar.setValue(100)
        self.eta_label.setText("ETA: 00:00")
        QMessageBox.information(self, "Success", f"Successfully downloaded {count} files!")

    def show_error(self, msg):
        self.cancel_btn.hide()
        self.download_btn.setText("Download All")
        self.download_btn.setEnabled(True)
        QMessageBox.critical(self, "Download Error", msg)

    def load_real_photos(self):
        # Clear existing items (Cache clearing)
        self.photo_list.clear()
        
        bucket_name = "calin-fotos-2026"
        # We'll use a temporary downloader or client to list
        # For simplicity in this UI update, we'll do a quick scan
        temp_loader = GCSDownloader(bucket_name, "")
        files = temp_loader.list_files()
        
        if not files:
            self.add_placeholder_items()
            return
            
        for file_name in files:
            item = QListWidgetItem(file_name)
            item.setTextAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
            # Use a default cloud icon for real files since we don't have thumbnails yet
            self.photo_list.addItem(item)
            
        # Update progress label to reflect real count
        progress_label = self.findChild(QLabel, "ProgressLabel")
        if progress_label:
            progress_label.setText(f"Scanning complete: {len(files)} files found in cloud.")

    def load_mock_photos(self):
        self.load_real_photos()
            
    def add_placeholder_items(self):
        # Adding empty placeholders just to see layout if assets aren't downloaded yet
        for i in range(12):
            item = QListWidgetItem(f"IMG_{1000+i}.raw")
            item.setTextAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
            self.photo_list.addItem(item)

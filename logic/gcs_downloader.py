from PyQt6.QtCore import QThread, pyqtSignal
from google.cloud import storage
from google.cloud.exceptions import NotFound, Forbidden
import os

class GCSDownloader(QThread):
    # Signals
    # Signals: current_bytes, total_bytes, current_file_name, current_count, total_count, speed_bps
    progress_updated = pyqtSignal(int, int, str, int, int, float) 
    download_finished = pyqtSignal(int)          # total_files_downloaded
    download_cancelled = pyqtSignal()            # Signal for cancellation
    error_occurred = pyqtSignal(str)             # error_message
    
    def __init__(self, bucket_name, target_dir):
        super().__init__()
        self.bucket_name = bucket_name
        self.target_dir = target_dir
        self._is_cancelled = False
        import time
        self.start_time = None
        if self.target_dir:
            os.makedirs(self.target_dir, exist_ok=True)
        
    def stop(self):
        self._is_cancelled = True

    def run(self):
        import time
        import shutil
        try:
            # Reassurance/Disk Space Check
            if self.target_dir:
                usage = shutil.disk_usage(os.path.abspath(self.target_dir))
                free_gb = usage.free / (1024**3)
                if free_gb < 60:
                     self.error_occurred.emit(f"Warning: Low disk space! {free_gb:.1f} GB available, 60 GB recommended.")
                     # We don't stop here, but notify. Or we can stop if it's too low.
            
            self.start_time = time.time()
            creds_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "credentials.json"))
            if os.path.exists(creds_path):
                client = storage.Client.from_service_account_json(creds_path)
            else:
                client = storage.Client()
                
            bucket_name = self.bucket_name if self.bucket_name else "calin-fotos-2026"
            bucket = client.get_bucket(bucket_name)
            
            blobs = list(bucket.list_blobs())
            if not blobs:
                self.download_finished.emit(0)
                return
                
            total_sz = sum(b.size for b in blobs if b.size)
            downloaded_bytes = 0
            downloaded_count = 0
            
            # Open log file
            log_path = os.path.join(self.target_dir, "..", "transfer_log.txt")
            
            with open(log_path, 'a', encoding='utf-8') as log_file:
                for blob in blobs:
                    if self._is_cancelled:
                        self.download_cancelled.emit()
                        return

                    if blob.name.endswith('/'):
                        continue # Skip directories
                        
                    file_path = os.path.join(self.target_dir, blob.name.replace('/', os.sep))
                    # Ensure subdirectories exist
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    try:
                        elapsed = time.time() - self.start_time
                        speed = downloaded_bytes / elapsed if elapsed > 0 else 0
                        self.progress_updated.emit(downloaded_bytes, total_sz, blob.name, downloaded_count, len(blobs), speed)
                        blob.download_to_filename(file_path)
                        downloaded_bytes += blob.size if blob.size else 0
                        downloaded_count += 1
                        log_file.write(f"SUCCESS: {blob.name}\n")
                        
                    except OSError as e:
                        if e.errno == 28 or "No space left" in str(e):
                            msg = f"Disk full while downloading {blob.name}"
                            log_file.write(f"ERROR: {msg}\n")
                            self.error_occurred.emit(msg)
                            return
                        else:
                            msg = f"OS Error downloading {blob.name}: {str(e)}"
                            log_file.write(f"ERROR: {msg}\n")
                            self.error_occurred.emit(msg)
                            return
                    except Exception as e:
                        msg = f"Failed to download {blob.name}: {str(e)}"
                        log_file.write(f"ERROR: {msg}\n")
                        self.error_occurred.emit(msg)
                        return
                        
            self.download_finished.emit(downloaded_count)
            
        except NotFound as e:
            self.error_occurred.emit(f"Bucket not found or 404: {str(e)}")
        except Forbidden as e:
            self.error_occurred.emit(f"Access denied or Forbidden 403: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"General Error: {str(e)}")

    def list_files(self):
        """Helper to list files without downloading them"""
        try:
            creds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "credentials.json")
            if os.path.exists(creds_path):
                client = storage.Client.from_service_account_json(creds_path)
            else:
                client = storage.Client()
                
            bucket = client.get_bucket(self.bucket_name if self.bucket_name else "calin-fotos-2026")
            blobs = list(bucket.list_blobs())
            return [b.name for b in blobs if not b.name.endswith('/')]
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

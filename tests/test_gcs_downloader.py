import pytest
import os
from unittest.mock import MagicMock, patch
from logic.gcs_downloader import GCSDownloader
from google.cloud.exceptions import NotFound, Forbidden

@pytest.fixture
def downloader():
    # Setup the downloader without starting the thread
    dl = GCSDownloader(bucket_name="test-bucket", target_dir="test_downloads")
    return dl

def test_bucket_not_found(downloader):
    """Test that error_occurred signal is emitted with proper message if bucket doesn't exist."""
    emitted_errors = []
    downloader.error_occurred.connect(lambda msg: emitted_errors.append(msg))
    
    with patch("logic.gcs_downloader.storage.Client") as mock_client_class:
        mock_client = mock_client_class.return_value
        # Simulate bucket lookup failing
        mock_client.get_bucket.side_effect = NotFound("Bucket test-bucket not found.")
        
        downloader.run()
        
        assert len(emitted_errors) == 1
        assert "not found" in emitted_errors[0].lower() or "not exist" in emitted_errors[0].lower() or "404" in emitted_errors[0]

def test_bucket_forbidden(downloader):
    """Test that error_occurred signal is emitted when bucket is private/forbidden."""
    emitted_errors = []
    downloader.error_occurred.connect(lambda msg: emitted_errors.append(msg))
    
    with patch("logic.gcs_downloader.storage.Client") as mock_client_class:
        mock_client = mock_client_class.return_value
        # Simulate forbidden access
        mock_client.get_bucket.side_effect = Forbidden("Access denied to test-bucket.")
        
        downloader.run()
        
        assert len(emitted_errors) == 1
        assert "access denied" in emitted_errors[0].lower() or "forbidden" in emitted_errors[0].lower() or "403" in emitted_errors[0]

def test_disk_full_error(downloader):
    """Test that OS Disk Full error is handled and emitted gracefully."""
    emitted_errors = []
    downloader.error_occurred.connect(lambda msg: emitted_errors.append(msg))
    
    with patch("logic.gcs_downloader.storage.Client") as mock_client_class:
        mock_client = mock_client_class.return_value
        mock_bucket = MagicMock()
        mock_client.get_bucket.return_value = mock_bucket
        
        mock_blob = MagicMock()
        mock_blob.name = "huge_file.zip"
        mock_blob.size = 1000000 
        mock_bucket.list_blobs.return_value = [mock_blob]
        
        # Simulate disk full (ENOSPC is usually error 28)
        # We can just raise an OSError with no space left message
        def mock_download_to_filename(filename):
            raise OSError(28, "No space left on device")
            
        mock_blob.download_to_filename.side_effect = mock_download_to_filename
        
        downloader.run()
        
        assert len(emitted_errors) == 1
        assert "disk full" in emitted_errors[0].lower() or "no space left" in emitted_errors[0].lower()


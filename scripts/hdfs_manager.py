import os
import sys

# Ensure hadoop module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hadoop import hdfs_config
from scripts.check_hdfs import check_hdfs_availability

class HDFSManager:
    def __init__(self):
        self.hdfs_command_available = check_hdfs_availability()
        
        # In future phases, we could try connecting, but for now we rely on command and config
        self.hdfs_connection_available = self.hdfs_command_available
        
        # Default to local mode if HDFS is unavailable or not enabled
        if self.hdfs_connection_available and hdfs_config.HDFS_ENABLED:
            self.mode = "hdfs"
        else:
            self.mode = "local"
            
    def get_mode(self):
        return self.mode
        
    def is_hdfs_available(self):
        return self.hdfs_connection_available
        
    def get_local_dataset_path(self):
        return hdfs_config.LOCAL_DATASET
        
    def get_hdfs_dataset_path(self):
        return f"{hdfs_config.HDFS_RAW_DIR}/retail_logs.csv"

manager = HDFSManager()
MODE = manager.get_mode()

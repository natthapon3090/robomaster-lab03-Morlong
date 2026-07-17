# src/logger.py
import os
import csv
import time
from datetime import datetime

class DataLogger:
    def __init__(self, config):
        self.base_dir = config['paths']['raw_data_dir']
        self.run_dir = self._create_run_folder()
        self.file_path = None
        self.csv_file = None
        self.writer = None

    def _create_run_folder(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)
            
        existing_runs = [d for d in os.listdir(self.base_dir) if d.startswith('run')]
        run_number = len(existing_runs) + 1
        new_run_dir = os.path.join(self.base_dir, f"run{run_number}")
        os.makedirs(new_run_dir, exist_ok=True)
        return new_run_dir

    def start_logging(self, sensor_type="imu"):
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"log_{date_str}_{sensor_type}.csv"
        self.file_path = os.path.join(self.run_dir, filename)
        
        self.csv_file = open(self.file_path, mode='w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(['timestamp', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z'])
        print(f"[Logger] Started data log file at: {self.file_path}")

    def log_imu_data(self, acc, gyro):
        if self.writer:
            timestamp = int(time.time() * 1000)
            self.writer.writerow([timestamp, acc[0], acc[1], acc[2], gyro[0], gyro[1], gyro[2]])

    def stop_logging(self):
        if self.csv_file:
            self.csv_file.close()
            print(f"[Logger] Data log saved and closed safely.")
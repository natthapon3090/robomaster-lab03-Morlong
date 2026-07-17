# src/logger.py
import csv
import os
from datetime import datetime

class DataLogger:
    def __init__(self, config=None):
        # 1. จัดการโฟลเดอร์เก็บข้อมูล (data/raw/runX)
        if config and 'paths' in config:
            self.base_dir = config['paths']['raw_data_dir']
        else:
            self.base_dir = "data/raw"
            
        self.run_dir = self._create_run_folder()
        
        # 2. เปิดไฟล์เขียนแบบรวมไฟล์เดียวชื่อ movement_log.csv (ใส่ encoding='utf-8-sig' เพื่อให้ Excel อ่านภาษาไทยออก)
        self.file_path = os.path.join(self.run_dir, 'movement_log.csv')
        self.csv_file = open(self.file_path, mode='w', newline='', encoding='utf-8-sig')
        self.writer = csv.writer(self.csv_file)
        
        # 3. เขียนชื่อหัวคอลัมน์ภาษาไทยแบบ "แยกทุกแกน X, Y, Z และทุกเซนเซอร์" ชัดเจน
        self.writer.writerow([
            'เวลาบันทึก (timestamp)', 
            'เหตุการณ์ (event)', 
            'พิกัด X (เมตร)', 
            'พิกัด Y (เมตร)', 
            'เป้าหมายองศา Z', 
            'ความเร็วเคลื่อนที่ (xy_speed)', 
            'ความเร็วหมุน (z_speed)', 
            'ด้านที่/ขั้นตอน (step)', 
            'ทำซ้ำ (repeat)', 
            'องศาการหัน (Yaw)',
            'องศาการก้มเงย (Pitch)',
            'องศาการเอียง (Roll)',
            'ความเร่งแกน X (g)',
            'ความเร่งแกน Y (g)',
            'ความเร่งแกน Z (g)',
            'ความเร็วเชิงมุมแกน X (deg/s)',
            'ความเร็วเชิงมุมแกน Y (deg/s)',
            'ความเร็วเชิงมุมแกน Z (deg/s)',
            'ความเร็วล้อที่ 1 (rpm)',
            'ความเร็วล้อที่ 2 (rpm)',
            'ความเร็วล้อที่ 3 (rpm)',
            'ความเร็วล้อที่ 4 (rpm)',
            'บันทึกเพิ่มเติม (note)'
        ])
        
        print(f"[Logger] เริ่มต้นสร้างไฟล์ข้อมูลเดี่ยวแบบแยกคอลัมน์ภาษาไทย: {self.file_path}")

    def _create_run_folder(self):
        """ สร้างโฟลเดอร์รันแยกตามรอบของการทดสอบให้อัตโนมัติ """
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)
            
        existing_runs = [d for d in os.listdir(self.base_dir) if d.startswith('run')]
        run_number = len(existing_runs) + 1
        new_run_dir = os.path.join(self.base_dir, f"run{run_number}")
        os.makedirs(new_run_dir, exist_ok=True)
        return new_run_dir

    def log_movement(self, event, x, y, z, xy_speed, z_speed, step, repeat, 
                     yaw, pitch, roll, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z,
                     speed_1, speed_2, speed_3, speed_4, note):
        """ ฟังก์ชันบันทึกข้อมูลแบบแยกคอลัมน์ครบถ้วนลงตารางเดียวจบ """
        # บันทึกรูปแบบเวลาเดียวกับในรูปภาพ (เช่น 2026-07-17T21:...)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        # เขียนแถวข้อมูลลง CSV ตามหัวข้อที่แยกไว้
        self.writer.writerow([
            timestamp, event, x, y, z, xy_speed, z_speed, step, repeat,
            yaw, pitch, roll, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z,
            speed_1, speed_2, speed_3, speed_4, note
        ])

    def close_files(self):
        """ ปิดไฟล์ข้อมูลอย่างปลอดภัยเมื่อจบการทำงาน """
        if self.csv_file:
            self.csv_file.close()
            print(f"[สำเร็จ] บันทึกไฟล์ข้อมูลแยกคอลัมน์ {self.file_path} เรียบร้อยแล้ว ภาษาไทยเปิดอ่านง่ายชัวร์!")
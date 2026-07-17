# src/logger.py
import csv
import time

class DataLogger:
    def __init__(self):
        # กำหนดให้บันทึกลงไฟล์เดี่ยว movement_log.csv ทันที
        self.file_path = "movement_log.csv"
        self.csv_file = None
        self.writer = None

    def start_logging(self):
        # เปิดไฟล์เขียนข้อมูลใหม่ทุกครั้งที่เริ่มรัน
        self.csv_file = open(self.file_path, mode='w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.csv_file)
        
        # ตั้งชื่อหัวคอลัมน์เหมือนใน Excel เป๊ะๆ
        self.writer.writerow(['timestamp', 'event', 'x', 'y', 'z', 'xy_speed', 'z_speed', 'step', 'note'])
        print(f"[Logger] ไฟล์บันทึกถูกสร้างขึ้นที่: {self.file_path}")

    def log_movement(self, event, x, y, z, xy_speed, z_speed, step, note):
        if self.writer:
            # ดึงเวลาปัจจุบันมาสร้าง timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            self.writer.writerow([timestamp, event, x, y, z, xy_speed, z_speed, step, note])
            # บังคับบันทึกข้อมูลลงไฟล์ทันที ป้องกันข้อมูลค้างหรือสูญหาย
            self.csv_file.flush() 

    def stop_logging(self):
        if self.csv_file:
            self.csv_file.close()
            print("[Logger] ปิดไฟล์บันทึกข้อมูลเรียบร้อยแล้ว")
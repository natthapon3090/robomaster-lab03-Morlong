import time
import csv
import os

class DataLogger:
    def __init__(self):
        # สร้างโฟลเดอร์ data อัตโนมัติหากยังไม่มีอยู่
        os.makedirs("data", exist_ok=True)
        
        # เปิดไฟล์เขียนแบบ CSV ทั้งหมด 5 ไฟล์
        self.f_att = open('data/log_attitude.csv', mode='w', newline='')
        self.f_pos = open('data/log_position.csv', mode='w', newline='')
        self.f_imu = open('data/log_imu.csv', mode='w', newline='')
        self.f_esc = open('data/log_esc.csv', mode='w', newline='')
        self.f_lat = open('data/log_latency.csv', mode='w', newline='')
        
        self.w_att = csv.writer(self.f_att)
        self.w_pos = csv.writer(self.f_pos)
        self.w_imu = csv.writer(self.f_imu)
        self.w_esc = csv.writer(self.f_esc)
        self.w_lat = csv.writer(self.f_lat)
        
        # เขียนชื่อคอลัมน์ (Headers) ของข้อมูล
        self.w_att.writerow(['timestamp', 'yaw', 'pitch', 'roll'])
        self.w_pos.writerow(['timestamp', 'x', 'y'])
        self.w_imu.writerow(['timestamp', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z'])
        self.w_esc.writerow(['timestamp', 'speed_1', 'speed_2', 'speed_3', 'speed_4'])
        self.w_lat.writerow(['timestamp', 'latency_ms'])

    # --- ฟังก์ชัน Callback สำหรับบันทึกแต่ละเซนเซอร์พร้อม Unix Timestamp ---
    
    def log_attitude(self, data):
        start_time = time.perf_counter()
        yaw, pitch, roll = data
        timestamp = int(time.time() * 1000)
        self.w_att.writerow([timestamp, yaw, pitch, roll])
        
        # คำนวณความหน่วงการรับส่งข้อมูล (Latency) สำหรับ Lab Assignment 2
        latency = (time.perf_counter() - start_time) * 1000
        self.w_lat.writerow([timestamp, latency])

    def log_position(self, data):
        x, y, _ = data
        self.w_pos.writerow([int(time.time() * 1000), x, y])

    def log_imu(self, data):
        acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = data
        self.w_imu.writerow([int(time.time() * 1000), acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z])

    def log_esc(self, data):
        speed_1, speed_2, speed_3, speed_4 = data
        self.w_esc.writerow([int(time.time() * 1000), speed_1, speed_2, speed_3, speed_4])

    def close_files(self):
        self.f_att.close()
        self.f_pos.close()
        self.f_imu.close()
        self.f_esc.close()
        self.f_lat.close()
        print("[สำเร็จ] บันทึกไฟล์ CSV ครบทั้ง 5 ไฟล์เรียบร้อยแล้วในโฟลเดอร์ data/")
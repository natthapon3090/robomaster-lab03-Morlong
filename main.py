# main.py
import time
from robomaster import robot
from src.config_loader import load_config
from src.logger import DataLogger
from src.chassis import ChassisController

if __name__ == '__main__':
    # 1. โหลดค่าคอนฟิกจากการตั้งค่า
    config = load_config()
    
    # 2. เริ่มต้นระบบเชื่อมต่อตัวหุ่นยนต์ (AP Mode)
    ep_robot = robot.Robot()
    
    # แก้ไขบรรทัดที่ 13 เป็นแบบนี้:
    ep_robot.initialize(conn_type="ap")
    
    # [Lab02 Checkpoint 1] ตรวจสอบและแสดงเวอร์ชันออกหน้าจอคอนโซล
    version = ep_robot.get_version()
    print(f"เวอร์ชันของหุ่นยนต์ (Robot Version): {version}")

    # 3. เริ่มต้นเปิดตัวบันทึกและสมัครรับข้อมูลเซนเซอร์ (Subscribe)
    logger = DataLogger()
    ep_chassis = ep_robot.chassis
    freq = config['robot']['sample_freq']

    # --- ส่วนที่เพิ่มเข้ามาเพื่อรวมข้อมูลเซนเซอร์ต่าง ๆ ลงไฟล์เดี่ยว (ตามรูปแบบที่คุณกำหนด) ---
    # ใช้ค่าเริ่มต้นชั่วคราวเพื่อให้ข้อมูลไม่ว่างเปล่า
    state = {"x": 0.0, "y": 0.0, "yaw": 0.0}

    def handle_attitude(data):
        yaw, pitch, roll = data
        state["yaw"] = yaw
        # บันทึกข้อมูลทิศทาง
        logger.log_movement(
            event="attitude_update", 
            x=state["x"], y=state["y"], z=yaw, 
            xy_speed=config['robot']['speed'], z_speed="", 
            step="-", repeat="-", note="reading attitude"
        )

    def handle_position(data):
        x, y, _ = data
        state["x"] = x
        state["y"] = y
        # บันทึกข้อมูลพิกัด位置
        logger.log_movement(
            event="position_update", 
            x=x, y=y, z=state["yaw"], 
            xy_speed=config['robot']['speed'], z_speed="", 
            step="-", repeat="-", note="reading position"
        )

    def handle_imu(data):
        # ดักข้อมูล IMU มาลงไฟล์เดี่ยว
        logger.log_movement(
            event="imu_update", 
            x=state["x"], y=state["y"], z=state["yaw"], 
            xy_speed=config['robot']['speed'], z_speed="", 
            step="-", repeat="-", note="reading imu"
        )

    def handle_esc(data):
        # ดักข้อมูลความเร็วล้อมาลงไฟล์เดี่ยว
        logger.log_movement(
            event="esc_update", 
            x=state["x"], y=state["y"], z=state["yaw"], 
            xy_speed=config['robot']['speed'], z_speed="", 
            step="-", repeat="-", note="reading esc"
        )

    # เปลี่ยน callback มาใช้ฟังก์ชันแปลงข้อมูลที่เราสร้างขึ้นด้านบนแทนของเก่าที่ไม่มีแล้ว
    ep_chassis.sub_attitude(freq=freq, callback=handle_attitude)
    ep_chassis.sub_position(freq=freq, callback=handle_position)
    ep_chassis.sub_imu(freq=freq, callback=handle_imu)
    ep_chassis.sub_esc(freq=freq, callback=handle_esc)
    
    time.sleep(1.0) # รอเวลาให้สัญญาณเซนเซอร์สเตเบิล
    
    # 4. เรียกทำงานชุดเคลื่อนฐานล้อตามรูปแบบสี่เหลี่ยม (ทำงานเหมือนเดิมทุกประการ)
    controller = ChassisController(
        ep_chassis=ep_chassis,
        tile_size=config['robot']['tile_size'],
        speed=config['robot']['speed']
    )
    
    print("\n=== เริ่มต้นเคลื่อนที่รูปสี่เหลี่ยม 2x2 ช่องกระเบื้อง ===")
    controller.execute_square_path()
    print("=== สิ้นสุดภารกิจเดินสี่เหลี่ยมเรียบร้อยแล้ว ===\n")

    # 5. ยกเลิกดักข้อมูลทั้งหมด ปิดหุ่นยนต์ และเซฟไฟล์ปิดท้าย
    ep_chassis.unsub_all()
    ep_robot.close()
    logger.close_files()
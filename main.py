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
    ep_robot.initialize(conn_type="rndis")
    
    # [Lab02 Checkpoint 1] ตรวจสอบและแสดงเวอร์ชันออกหน้าจอคอนโซล
    version = ep_robot.get_version()
    print(f"เวอร์ชันของหุ่นยนต์ (Robot Version): {version}")

    # 3. เริ่มต้นเปิดตัวบันทึกและสมัครรับข้อมูลเซนเซอร์ (Subscribe)
    logger = DataLogger()
    ep_chassis = ep_robot.chassis
    freq = config['robot']['sample_freq']

    ep_chassis.sub_attitude(freq=freq, callback=logger.log_attitude)
    ep_chassis.sub_position(freq=freq, callback=logger.log_position)
    ep_chassis.sub_imu(freq=freq, callback=logger.log_imu)
    ep_chassis.sub_esc(freq=freq, callback=logger.log_esc)
    
    time.sleep(1.0) # รอเวลาให้สัญญาณเซนเซอร์สเตเบิล
    
    # 4. เรียกทำงานชุดเคลื่อนฐานล้อตามรูปแบบสี่เหลี่ยม
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
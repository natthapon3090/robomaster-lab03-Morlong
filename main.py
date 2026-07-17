# main.py
from robomaster import robot
from src.config_loader import load_settings
from src.chassis import ChassisController
from src.logger import DataLogger

def main():
    # 1. โหลดค่าตั้งค่าจาก settings.yaml
    config = load_settings()
    conn_mode = config['connection']['mode']
    
    # 2. เปิดระบบ Logger บันทึกไฟล์เดี่ยว
    logger = DataLogger()
    logger.start_logging()
    
    # 3. เตรียมเชื่อมต่อหุ่นยนต์
    print(f"[Main] กำลังเชื่อมต่อ RoboMaster ผ่านโหมด: {conn_mode.upper()}...")
    ep_robot = robot.Robot()
    
    try:
        ep_robot.initialize(conn_type=conn_mode)
        print("[Main] เชื่อมต่อหุ่นยนต์สำเร็จ!")
        
        # 4. ส่งค่า config เข้าไปให้ ChassisController นำความเร็วไปใช้
        chassis_ctrl = ChassisController(ep_robot, logger, config)
        print("[Main] เริ่มทำภารกิจวิ่งรูปสี่เหลี่ยมจัตุรัส 2x2 tile...")
        chassis_ctrl.execute_square_path()
            
        print("[Main] ภารกิจสำเร็จลุล่วงด้วยดี!")
        
    except KeyboardInterrupt:
        print("\n[Main] โปรแกรมหยุดทำงานเนื่องจากผู้ใช้กดหยุด (Ctrl+C)")
    except Exception as e:
        print(f"[Main] เกิดข้อผิดพลาดขึ้น: {e}")
    finally:
        # 5. เคลียร์ระบบและปิดการใช้งานอย่างปลอดภัย
        print("[Main] กำลังเคลียร์ระบบและตัดการเชื่อมต่อ...")
        logger.stop_logging()
        
        try:
            ep_robot.close()
        except:
            pass
            
        print("[Main] ปิดระบบเรียบร้อย โค้ดจบการทำงานอย่างสมบูรณ์")

if __name__ == "__main__":
    main()
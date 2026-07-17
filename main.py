# main.py
import time
from robomaster import robot
from src.config_loader import load_settings
from src.chassis import ChassisController
from src.logger import DataLogger

def main():
    config = load_settings()
    conn_mode = config['connection']['mode']
    logger = DataLogger(config)
    
    print(f"[Main] Initializing RoboMaster via Mode: {conn_mode.upper()}...")
    ep_robot = robot.Robot()
    
    try:
        ep_robot.initialize(conn_type=conn_mode)
        print("[Main] Connected successfully! SN:", ep_robot.get_sn())
        
        chassis_ctrl = ChassisController(ep_robot, config)
        logger.start_logging(sensor_type="imu")
        
        # --- เริ่มโปรโตคอลเคลื่อนที่และเลี้ยว ---
        
        # 1. เดินหน้า 0.5 เมตร
        chassis_ctrl.move_forward(distance=0.5)
        logger.log_imu_data(acc=[0.1, 0.02, 9.8], gyro=[0.0, 1.2, -0.5])
        time.sleep(0.5)
        
        # 2. เลี้ยวซ้ายทำมุม 90 องศา
        chassis_ctrl.turn(degree=90)
        logger.log_imu_data(acc=[0.15, 0.1, 9.78], gyro=[0.0, 0.0, 30.0]) # จำลองค่า Gyro แกน Z ขยับขณะเลี้ยว
        time.sleep(0.5)
        
        # 3. เดินหน้าต่ออีก 0.5 เมตร ในทิศทางใหม่หลังจากเลี้ยวแล้ว
        chassis_ctrl.move_forward(distance=0.5)
        logger.log_imu_data(acc=[0.09, 0.01, 9.81], gyro=[0.1, 0.8, 0.0])
        time.sleep(0.5)
            
        print("[Main] Mission completed successfully.")
        
    except KeyboardInterrupt:
        print("\n[Main] Execution interrupted by User (Ctrl+C).")
    except Exception as e:
        print(f"[Main] Error encountered during execution: {e}")
    finally:
        print("[Main] Executing cleanup phase...")
        logger.stop_logging()
        try:
            ep_robot.camera.stop_video_stream()
        except:
            pass
        ep_robot.uninitialize()
        print("[Main] Robot disconnected cleanly. System shutdown.")

if __name__ == "__main__":
    main()
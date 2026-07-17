# src/chassis.py
import time

class ChassisController:
    def __init__(self, ep_robot, logger_object, config):
        # ดึงคำสั่งควบคุมล้อ
        self.chassis = ep_robot.chassis
        self.logger = logger_object
        
        # ดึงค่าความเร็วและระยะทางมาจากไฟล์ settings.yaml
        self.tile_size = config['robot_settings']['tile_size']
        self.speed = config['robot_settings']['speed']
        self.turn_speed = config['robot_settings']['turn_speed']

    def execute_square_path(self):
        # วนลูปทำงานทั้งหมด 4 ด้าน (ครบสี่เหลี่ยมพอดี)
        for side in range(4):
            step_num = side + 1
            print(f"\n==========================================")
            print(f"[Chassis] เริ่มทำงานด้านที่ {step_num}")
            print(f"==========================================")

            # --------------------------------------------------------
            # 1. จังหวะเดินหน้าตรงทีละช่อง (ทั้งหมด 2 ช่อง)
            # --------------------------------------------------------
            for i in range(2):
                tile_num = i + 1
                print(f"-> [เดินหน้า] ช่องที่ {tile_num} ของด้านที่ {step_num}")
                
                # สั่งหุ่นเดินหน้า (+X) ด้วยความเร็วที่ตั้งไว้
                self.chassis.move(x=self.tile_size, y=0, z=0, xy_speed=self.speed).wait_for_completed()
                
                # บันทึกข้อมูลลง CSV
                self.logger.log_movement(
                    event="move_forward", 
                    x=self.tile_size, y=0, z=0, 
                    xy_speed=self.speed, z_speed="", 
                    step=step_num, note="forward"
                )
                time.sleep(1.0) # หยุดนิ่ง 1 วินาทีเมื่อวิ่งเสร็จ 1 ช่อง

            # --------------------------------------------------------
            # 2. จังหวะเลี้ยวขวา 90 องศา (หลังจากวิ่งครบ 2 ช่อง)
            # --------------------------------------------------------
            print(f"-> [เลี้ยวขวา] หมุนขวา 90 องศา")
            
            # บันทึกตอนเริ่มเลี้ยว (turn_start)
            self.logger.log_movement(
                event="turn_start", 
                x=0, y=0, z=-90, 
                xy_speed="", z_speed=self.turn_speed, 
                step=step_num, note="turn"
            )
            
            # สั่งหุ่นหมุนขวาตามเข็มนาฬิกา (z ติดลบ -90)
            self.chassis.move(x=0, y=0, z=-90, z_speed=self.turn_speed).wait_for_completed()
            
            # บันทึกตอนเลี้ยวเสร็จ (turn_end)
            self.logger.log_movement(
                event="turn_end", 
                x=0, y=0, z=-90, 
                xy_speed="", z_speed=self.turn_speed, 
                step=step_num, note="turn"
            )
            time.sleep(1.0) # หยุดนิ่งอีก 1 วินาทีหลังเลี้ยวเสร็จ

        print("\n[Chassis] วิ่งครบสี่เหลี่ยมจัตุรัส 4 ด้าน เรียบร้อยแล้ว!")
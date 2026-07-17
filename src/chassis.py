import time

class ChassisController:
    def __init__(self, ep_chassis, tile_size, speed):
        self.chassis = ep_chassis
        self.tile_size = tile_size
        self.speed = speed

    def execute_square_path(self):
        """
        วิ่งเป็นรูปสี่เหลี่ยมจัตุรัสโดยการ เดินหน้าตรง -> เลี้ยวซ้าย 90 องศา 
        ทำซ้ำทั้งหมด 4 ด้านเพื่อกลับมาที่จุดเริ่มต้นในทิศทางเดิม
        """
        # วนลูป 4 ด้านของสี่เหลี่ยมจัตุรัส
        for side in range(4):
            print(f"\n--- กำลังวิ่งด้านที่ {side + 1} ---")
            
            # 1. เดินหน้าตรง (+X) จำนวน 2 ช่องกระเบื้อง
            for i in range(2):
                print(f"-> กำลังเดินหน้า: ช่องที่ {i+1}")
                self.chassis.move(x=self.tile_size, y=0, z=0, xy_speed=self.speed).wait_for_completed()
                time.sleep(0.5) # หยุดนิ่ง 1 วินาที
            
            # 2. เลี้ยวซ้าย 90 องศา (เปลี่ยนพารามิเตอร์ความเร็วเป็น xy_speed เรียบร้อย)
            print(f"-> กำลังเลี้ยวซ้าย 90 องศา")
            self.chassis.move(x=0, y=0, z=-90, xy_speed=self.speed).wait_for_completed()
            time.sleep(0.5) # หยุดนิ่งให้หุ่นนิ่งหลังเลี้ยว
            
        print("\n[Chassis] วิ่งครบสี่เหลี่ยมจัตุรัสและกลับสู่จุดเริ่มต้นเรียบร้อย!")
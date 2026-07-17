import time

class ChassisController:
    def __init__(self, ep_chassis, tile_size, speed):
        self.chassis = ep_chassis
        self.tile_size = tile_size
        self.speed = speed

    def execute_square_path(self):
        # 1. เดินหน้าตรง (+X) จำนวน 2 ช่องกระเบื้อง
        for i in range(2):
            print(f"-> กำลังเดินหน้า: ช่องที่ {i+1}")
            self.chassis.move(x=self.tile_size, y=0, z=0, xy_speed=self.speed).wait_for_completed()
            time.sleep(1.0) # หยุดนิ่ง 1 วินาที

        # 2. สไลด์ด้านข้างไปทิศทางขวา (+Y) จำนวน 2 ช่องกระเบื้อง
        for i in range(2):
            print(f"-> กำลังสไลด์ไปทางขวา: ช่องที่ {i+1}")
            self.chassis.move(x=0, y=self.tile_size, z=0, xy_speed=self.speed).wait_for_completed()
            time.sleep(1.0)

        # 3. ถอยหลังตรง (-X) จำนวน 2 ช่องกระเบื้อง
        for i in range(2):
            print(f"-> กำลังถอยหลัง: ช่องที่ {i+1}")
            self.chassis.move(x=-self.tile_size, y=0, z=0, xy_speed=self.speed).wait_for_completed()
            time.sleep(1.0)

        # 4. สไลด์ด้านข้างไปทิศทางซ้าย (-Y) จำนวน 2 ช่องกระเบื้องเพื่อกลับจุดเริ่มต้น
        for i in range(2):
            print(f"-> กำลังสไลด์ไปทางซ้ายกลับจุดเริ่ม: ช่องที่ {i+1}")
            self.chassis.move(x=0, y=-self.tile_size, z=0, xy_speed=self.speed).wait_for_completed()
            time.sleep(1.0)
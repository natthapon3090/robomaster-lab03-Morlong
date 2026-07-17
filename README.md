# RoboMaster Lab 03 – Lab Assignment 1: API Testing

## สมาชิกในกลุ่ม
| ชื่อ-นามสกุล | รหัสนักศึกษา | หน้าที่ |
|---|---|---|
| (ใส่ชื่อ) | (ใส่รหัส) | (เช่น เขียนโค้ด chassis, logger) |
| (ใส่ชื่อ) | (ใส่รหัส) | |
| (ใส่ชื่อ) | (ใส่รหัส) | |

## รายละเอียดงาน (Lab assignment 1: API testing)
1. วางหุ่นยนต์ไว้กึ่งกลาง tile ตั้งต้น แล้วสั่งให้หุ่นยนต์เดินเป็นเส้นทางสี่เหลี่ยมจัตุรัสขนาด 2x2 tile
   โดยหุ่นยนต์ต้อง**เดินหน้าตลอด** (ไม่หมุนตัว ใช้การสไลด์ล้อ Mecanum) ตามรูปในเอกสารโจทย์
   (ขึ้น 2 ช่อง → ขวา 2 ช่อง → ลง 2 ช่อง → ซ้าย 2 ช่อง กลับที่เดิม)
2. ระหว่างที่หุ่นยนต์เคลื่อนที่ ให้บันทึกค่าจากเซนเซอร์ทั้งหมด (position, attitude, IMU, battery ฯลฯ)
   พร้อม timestamp / time step ลง console และไฟล์ `.csv`
3. หยุดหุ่นยนต์ 1 วินาทีทุกครั้งที่เดินครบ 1 tile
4. นำข้อมูลจากไฟล์ `.csv` มาพล็อตกราฟแยก pane ตามชนิดของเซนเซอร์ โดยแกน X คือ time step

## โครงสร้างโปรเจกต์
```
robomaster-lab03-ชื่อกลุ่ม/
├── .venv/
├── .gitignore
├── requirements.txt
├── README.md
├── main.py                  # Entry point สั่งหุ่นยนต์วิ่งเป็นสี่เหลี่ยม 2x2 tile + log ข้อมูล
├── config/
│   └── settings.yaml        # พารามิเตอร์ของหุ่นยนต์และ path ต่างๆ
├── src/
│   ├── __init__.py
│   ├── config_loader.py     # โหลด settings.yaml เป็น dict
│   ├── chassis.py           # คลาสควบคุมล้อ Mecanum (เดินหน้า/ถอย/สไลด์ทีละ tile)
│   ├── gimbal.py            # คลาสควบคุมป้อมปืน/กล้อง
│   ├── vision.py            # คลาสสตรีมภาพ/ประมวลผลกล้อง (OpenCV)
│   └── logger.py            # คลาสบันทึกข้อมูลเซนเซอร์ลง CSV แบบเรียลไทม์
├── data/
│   ├── raw/                 # ไฟล์ CSV ดิบ แยกตาม run
│   └── processed/           # ไฟล์ที่ผ่านการกรองแล้ว (ถ้ามี)
└── analysis/
    ├── analyze_logs.ipynb   # โน้ตบุ๊กพล็อตกราฟจากไฟล์ CSV
    └── plots/                # รูปกราฟที่ export ออกมา
```

## วิธีติดตั้ง
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
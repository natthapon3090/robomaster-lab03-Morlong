# src/config_loader.py
import yaml
import os

def load_settings(config_path="config/settings.yaml"):
    """ โหลดไฟล์คอนฟิก YAML และแปลงเป็น Python Dictionary """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"ไม่พบไฟล์คอนฟิกที่ตำแหน่ง: {config_path}")
        
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config
    except Exception as e:
        raise RuntimeError(f"เกิดข้อผิดพลาดในการอ่านไฟล์ YAML: {e}")
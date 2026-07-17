import yaml

def load_config(config_path="config/settings.yaml"):
    # เพิ่ม encoding="utf-8" เข้าไปในบรรทัดด้านล่างนี้
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
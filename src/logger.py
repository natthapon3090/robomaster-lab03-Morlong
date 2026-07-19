import csv
import os

# ==========================
# CSV Files
# ==========================

POSITION_FILE = "data/raw/position_log.csv"
ATTITUDE_FILE = "data/raw/attitude_log.csv"
IMU_FILE = "data/raw/imu_log.csv"
ESC_FILE = "data/raw/esc_log.csv"
GYRO_FILE = "data/raw/gyro_log.csv"
STATUS_FILE = "data/raw/chassis_status_log.csv"


# ==========================
# Create CSV Files
# ==========================

def create_csv():

    files = {
        POSITION_FILE: [
            "timestamp",
            "x",
            "y",
            "z"
        ],

        ATTITUDE_FILE: [
            "timestamp",
            "roll",
            "pitch",
            "yaw"
        ],

        IMU_FILE: [
            "timestamp",
            "acc_x",
            "acc_y",
            "acc_z"
        ],

        ESC_FILE: [
            "timestamp",
            "wheel1_speed",
            "wheel2_speed",
            "wheel3_speed",
            "wheel4_speed"
        ],

        GYRO_FILE: [
            "timestamp",
            "gyro_x",
            "gyro_y",
            "gyro_z"
        ],

        STATUS_FILE: [
            "timestamp",
            "status"
        ]
    }

    for filename, header in files.items():

        if not os.path.exists(filename):

            with open(filename, "w", newline="") as file:

                writer = csv.writer(file)
                writer.writerow(header)


# ==========================
# Save Position
# ==========================

def save_position(timestamp, x, y, z):

    with open(POSITION_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            x,
            y,
            z
        ])


# ==========================
# Save Attitude
# ==========================

def save_attitude(timestamp, roll, pitch, yaw):

    with open(ATTITUDE_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            roll,
            pitch,
            yaw
        ])


# ==========================
# Save IMU
# ==========================

def save_imu(timestamp, acc_x, acc_y, acc_z):

    with open(IMU_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            acc_x,
            acc_y,
            acc_z
        ])


# ==========================
# Save ESC
# ==========================

def save_esc(timestamp, wheel1, wheel2, wheel3, wheel4):

    with open(ESC_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            wheel1,
            wheel2,
            wheel3,
            wheel4
        ])


# ==========================
# Save Gyroscope
# ==========================

def save_gyro(timestamp, gyro_x, gyro_y, gyro_z):

    with open(GYRO_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            gyro_x,
            gyro_y,
            gyro_z
        ])


# ==========================
# Save Chassis Status
# ==========================

def save_status(timestamp, status):

    with open(STATUS_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            status
        ])
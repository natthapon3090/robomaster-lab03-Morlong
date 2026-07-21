import time

from src.logger import (
    save_position,
    save_attitude,
    save_imu,
    save_esc,
    save_gyro,
    save_status
)


# ==========================
# Callback Functions
# ==========================


def sub_position_handler(position_info):

    x, y, z = position_info

    save_position(
        time.time(),
        x,
        y,
        z
    )



def sub_attitude_handler(attitude_info):

    yaw, pitch, roll = attitude_info

    save_attitude(
        time.time(),
        roll,
        pitch,
        yaw
    )



def sub_imu_handler(imu_info):

    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = imu_info


    # Save IMU

    save_imu(
        time.time(),
        acc_x,
        acc_y,
        acc_z
    )


    # Save Gyroscope

    save_gyro(
        time.time(),
        gyro_x,
        gyro_y,
        gyro_z
    )



def sub_esc_handler(esc_info):

    speed, angle, timestamp, state = esc_info


    save_esc(
        time.time(),
        speed[0],
        speed[1],
        speed[2],
        speed[3]
    )



# ==========================
# Main Function
# ==========================


def move_square(ep_robot, config):

    chassis = ep_robot.chassis


    distance = config["robot"]["move_distance"]

    speed = config["robot"]["move_speed"]

    angle = config["robot"]["turn_angle"]

    turn_speed = config["robot"]["turn_speed"]

    stop_time = config["robot"]["stop_time"]



    # ==========================
    # Subscribe Sensors
    # ==========================

    chassis.sub_position(
        freq=10,
        callback=sub_position_handler
    )


    chassis.sub_attitude(
        freq=10,
        callback=sub_attitude_handler
    )


    chassis.sub_imu(
        freq=10,
        callback=sub_imu_handler
    )


    chassis.sub_esc(
        freq=10,
        callback=sub_esc_handler
    )



    # ==========================
    # Move Square
    # ==========================

    for i in range(4):


        print("Forward")


        # Save chassis status

        save_status(
            time.time(),
            "forward"
        )


        chassis.move(
            x=distance / 2,
            y=0,
            z=0,
            xy_speed=speed
        ).wait_for_completed()



        time.sleep(stop_time)



        save_status(
            time.time(),
            "forward"
        )


        chassis.move(
            x=distance / 2,
            y=0,
            z=0,
            xy_speed=speed
        ).wait_for_completed()



        time.sleep(stop_time)



        print("Turn Right")



        # Save chassis status

        save_status(
            time.time(),
            "turn_right"
        )


        chassis.move(
            x=0,
            y=0,
            z=angle,
            z_speed=turn_speed
        ).wait_for_completed()



        time.sleep(stop_time)



    # ==========================
    # Stop Status
    # ==========================

    save_status(
        time.time(),
        "stop"
    )



    # ==========================
    # Unsubscribe Sensors
    # ==========================


    chassis.unsub_position()

    chassis.unsub_attitude()

    chassis.unsub_imu()

    chassis.unsub_esc()
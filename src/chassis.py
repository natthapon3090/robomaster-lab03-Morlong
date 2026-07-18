import time

from src.logger import save_log


def move_square(ep_robot, config):

    chassis = ep_robot.chassis

    distance = config["robot"]["move_distance"]
    speed = config["robot"]["move_speed"]

    angle = config["robot"]["turn_angle"]
    turn_speed = config["robot"]["turn_speed"]

    stop_time = config["robot"]["stop_time"]

    step = 1

    for i in range(4):

        print("Forward")

        save_log(
            time.time(),
            "Forward",
            distance,
            0,
            0,
            speed,
            0,
            step,
            "Move 1 Tile"
        )

        chassis.move(
            x=distance/2,
            y=0,
            z=0,
            xy_speed=speed
        ).wait_for_completed()

        time.sleep(stop_time)
        chassis.move(
            x=distance/2,
            y=0,
            z=0,
            xy_speed=speed
        ).wait_for_completed()

        time.sleep(stop_time)

        step += 1

        print("Turn Right")

        save_log(
            time.time(),
            "Turn Right",
            0,
            0,
            angle,
            0,
            turn_speed,
            step,
            "Rotate 90 Degree"
        )

        chassis.move(
            x=0,
            y=0,
            z=angle,
            z_speed=turn_speed
        ).wait_for_completed()

        step += 1
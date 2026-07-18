from robomaster import robot

from src.logger import create_csv
from src.config_loader import load_config
from src.chassis import move_square


config = load_config()

create_csv()

ep_robot = robot.Robot()

ep_robot.initialize(conn_type="ap")

try:

    move_square(ep_robot, config)

finally:

    ep_robot.close()

    print("Finish")
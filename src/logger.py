import csv
import os

CSV_FILE = "data/raw/movement_log.csv"


def create_csv():

    if not os.path.exists(CSV_FILE):

        with open(CSV_FILE, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "event",
                "x",
                "y",
                "z",
                "xy_speed",
                "z_speed",
                "step",
                "note"
            ])


def save_log(timestamp,
             event,
             x,
             y,
             z,
             xy_speed,
             z_speed,
             step,
             note):

    with open(CSV_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            event,
            x,
            y,
            z,
            xy_speed,
            z_speed,
            step,
            note
        ])
import subprocess
import time
import requests
import logging

VERSION = "0.1.0"
LOW_THRESHOLD = 50
HIGH_THRESHOLD = 60

logging.basicConfig(
    level=logging.INFO,
    filename=f"/var/log/battery_saver/battery_saver_log.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
)


class Charger:
    def __init__(self, ip) -> None:
        self.__ip = ip

    def on(self):
        logging.info(f"charge on")
        requests.get(f"http://{self.__ip}/relay_off")

    def off(self):
        logging.info(f"charge off")
        requests.get(f"http://{self.__ip}/relay_on")


def get_battery_percentage() -> float:
    output = str(
        subprocess.check_output(
            ["upower", "-i", "/org/freedesktop/UPower/devices/battery_BAT0"]
        )
    )
    output = output.split("percentage:")[-1]
    output = output.split("%")[0]
    return float(output)


def main():
    logging.info(f"Battery saver {VERSION} start.")
    charger = Charger("192.168.1.56")
    while True:
        battery_percentage = get_battery_percentage()
        logging.info(f"{battery_percentage=}")
        if battery_percentage > HIGH_THRESHOLD:
            charger.off()
        elif battery_percentage < LOW_THRESHOLD:
            charger.on()
        time.sleep(60)


if __name__ == "__main__":
    main()

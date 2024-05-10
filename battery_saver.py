import subprocess
import time
import requests
import logging
import subprocess
from retry import retry

VERSION = "0.1.0"
LOW_THRESHOLD = 50
HIGH_THRESHOLD = 55

logging.basicConfig(
    level=logging.INFO,
    filename=f"/var/log/battery_saver/battery_saver_log.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
)


class Charger:
    def __init__(self, ip) -> None:
        self.__ip = ip

    @retry(ConnectionError, tries=10, delay=10)
    def __send_to_relay(self, endpoint: str):
        response = requests.get(f"http://{self.__ip}{endpoint}")
        if response.status_code != 200:
            logging.error(f"Relay not connection")
            raise ConnectionError()

    def __relay_execute(self, endpoint: str):
        try:
            self.__send_to_relay(endpoint)
        except Exception:
            # subprocess.Popen(
            #     [
            #         "notify-send",
            #         "Ошибка",
            #         "Нет связи с реле",
            #         "-u",
            #         "CRITICAL",
            #         "-i",
            #         "/usr/share/icons/hicolor/48x48/apps/gnome-power-manager.png",
            #     ]
            # )
            logging.critical(f"Relay not connection")

    def on(self):
        logging.info(f"charge on")
        self.__relay_execute("/relay_on")

    def off(self):
        logging.info(f"charge off")
        self.__relay_execute("/relay_off")


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
    logging.info(f"Battery saver version {VERSION} is started.")
    logging.info(f"Thresholds: {LOW_THRESHOLD}..{HIGH_THRESHOLD}.")
    charger = Charger("192.168.0.100")
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

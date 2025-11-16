import logging
import json

from services.backend import backend


handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s / %(name)s [%(asctime)s] %(message)s", datefmt="%H:%M:%S %d.%m.%Y"))

logger = logging.getLogger("bot")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


with open("./assets/langs/ru_RU.json") as file:
    t = json.loads(file.read())

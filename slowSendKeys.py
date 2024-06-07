import random
import time
from typing import Tuple

from selenium.webdriver.remote.webelement import WebElement


def slowSendKeys(
    element: WebElement, string: str, pauseRange: Tuple[float, float] = (0.05, 0.2)
):
    for char in string:
        element.send_keys(char)
        time.sleep(random.uniform(pauseRange[0], pauseRange[1]))

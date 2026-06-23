import logging
import random
import time

logger = logging.getLogger(__name__)


class RandomSleep:
    def __call__(self, base: float = 0.1, rand: float = 2.5):
        self.rand_sleep(base, rand)

    def rand_sleep(self, base, rand) -> None:
        random_sleep = base + rand * random.random()
        logger.info("RandomSleep: 随机休眠: %s", random_sleep)
        time.sleep(random_sleep)

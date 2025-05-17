import random
import time
import logging

class RandomSleep():
    def __call__(self, base: float = 0.1, rand: float = 2.5):
        self.rand_sleep(base, rand)

    def rand_sleep(self, base, rand) -> None:
        random_sleep = base + rand * random.random()
        logging.info("RandomSleep: 随机休眠: %s", random_sleep)
        time.sleep(random_sleep)
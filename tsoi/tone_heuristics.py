from collections import deque
from itertools import islice
from time import sleep

from scipy.stats import percentileofscore

from constants import SLEEP_TIME
from interruptions import interruption_iter


DEQUE_MAXLEN = 20


class ToneHeuristic:
    def warm_up(self):
        """
        Define this to calculate any values you need before returning
        actual notes.
        """
        pass

    def get_tone(self, num_interrupts):
        """
        This should return a float between 0 and 1 representing the pitch
        of the tone.
        """
        raise NotImplementedError()


class DivideByMaxHeuristic(ToneHeuristic):
    """
    Divide num of interruptions by max number of interruptions seen.

    This heuristic breaks after an event with a high number of
    interruptions, i.e. opening chrome.
    """

    def warm_up(self):
        self.deque = deque(maxlen=DEQUE_MAXLEN)
        for num_interrupts in islice(interruption_iter(), self.deque.maxlen):
            self.deque.append(num_interrupts)
            sleep(SLEEP_TIME)

    def get_tone(self, num_interrupts):
        self.deque.append(num_interrupts)
        return num_interrupts / max(self.deque)


class PercentileHeuristic(ToneHeuristic):
    """
    Keep a sample of interruption amounts, return percentile of
    interrupts.
    """

    def warm_up(self):
        self.deque = deque(maxlen=DEQUE_MAXLEN)
        for num_interrupts in islice(interruption_iter(), self.deque.maxlen):
            self.deque.append(num_interrupts)
            sleep(SLEEP_TIME)

    def get_tone(self, num_interrupts):
        self.deque.append(num_interrupts)
        return percentileofscore(self.deque, num_interrupts) / 100


HEURISTIC_OPTIONS = {
    '--max': DivideByMaxHeuristic,
    '--percentile': PercentileHeuristic,
}

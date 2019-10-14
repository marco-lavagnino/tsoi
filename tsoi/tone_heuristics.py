from constants import SLEEP_TIME
from scipy.stats import percentileofscore
from itertools import islice
from time import sleep
from interruptions import interruption_iter


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
    max_interrupts = 1

    def warm_up(self):
        for num_interrupts in islice(interruption_iter(), 50):
            self.max_interrupts = max(num_interrupts, self.max_interrupts)
            sleep(SLEEP_TIME)

    def get_tone(self, num_interrupts):
        if self.max_interrupts < num_interrupts:
            self.max_interrupts = num_interrupts

        return num_interrupts / self.max_interrupts


class PercentileHeuristic(ToneHeuristic):
    """
    Keep a sample of interruption amounts, return percentile of
    interrupts.
    """

    def warm_up(self):
        self.past_interrupts = []

        for num_interrupts in islice(interruption_iter(), 50):
            self.past_interrupts.append(num_interrupts)
            sleep(SLEEP_TIME)

    def get_tone(self, num_interrupts):
        if len(self.past_interrupts) < 512:
            self.past_interrupts.append(num_interrupts)

        return percentileofscore(self.past_interrupts, num_interrupts) / 100


HEURISTIC_OPTIONS = {
    '--max': DivideByMaxHeuristic,
    '--percentile': PercentileHeuristic,
}

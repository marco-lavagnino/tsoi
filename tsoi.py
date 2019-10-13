
from time import sleep
import re
from synthesizer import Player, Synthesizer, Waveform
from itertools import islice

'''
Let's use a pleasing representation of this signal.
source: https://pages.mtu.edu/~suits/notefreqs.html
'''
PIANO_C_SCALE = {
    'C1': 32.70,
    'E1': 41.20,
    'G1': 49.00,
    'C2': 65.41,
    'E2': 82.41,
    'G2': 98.00,
    'C3': 130.81,
    'E3': 164.81,
    'G3': 196.00,
    'C4': 261.63,
    'E4': 329.63,
    'G4': 392.00,
    'C5': 523.25,
    'E5': 659.25,
    'G5': 783.99,
    'C6': 1046.50,
    'E6': 1318.51,
    'G6': 1567.98,
    'C7': 2093.00,
    'E7': 2637.02,
    'G7': 3135.96,
    'C8': 4186.01,
    'E8': 5274.04,
    'G8': 6271.93,
}
TONES = list(PIANO_C_SCALE.values())

SLEEP_TIME = 0.05


def get_number_of_cores():
    with open('/proc/interrupts') as f:
        contents = f.read()

        return len(contents.split('\n')[0].split())


NUMBER_OF_CORES = get_number_of_cores()


def get_interruptions():
    interruptions = 0
    with open('/proc/interrupts') as f:
        contents = f.read()

        for line in contents.split('\n')[1:]:
            columns = line.split()
            if len(columns) < NUMBER_OF_CORES + 1:
                continue

            interruptions += sum(
                int(n) for n
                in columns[1:NUMBER_OF_CORES + 1]
            )

    return interruptions


def interruption_iter():
    last_interruptions = get_interruptions()
    while True:
        current_interruptions = get_interruptions()
        yield current_interruptions - last_interruptions
        last_interruptions = current_interruptions


def get_max_interrupts():
    max_interrupts = 1

    for num_interrupts in islice(interruption_iter(), 10):
        max_interrupts = max(num_interrupts, max_interrupts)
        sleep(SLEEP_TIME)

    return max_interrupts


player = Player()

player.open_stream()
synthesizer = Synthesizer(
    osc1_waveform=Waveform.sine,
    osc1_volume=1.0,
    use_osc2=False,
)


max_interrupts = get_max_interrupts()

for num_interrupts in interruption_iter():
    if max_interrupts < num_interrupts:
        max_interrupts = num_interrupts

    tone_num = round(num_interrupts / max_interrupts * (len(TONES)-1))
    print(tone_num, max_interrupts)
    # sleep(SLEEP_TIME)
    tone = synthesizer.generate_constant_wave(TONES[tone_num], SLEEP_TIME)
    player.play_wave(tone)

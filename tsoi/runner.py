from queue import Queue
from threading import Thread

from constants import SLEEP_TIME, TONES
from interruptions import interruption_iter
from synthesizer import Player, Synthesizer, Waveform


def producer(queue, tone_heuristic):
    synthesizer = Synthesizer(
        osc1_waveform=Waveform.square,
        osc1_volume=1.0,
        use_osc2=False,
    )
    tone_heuristic.warm_up()

    for num_interrupts in interruption_iter():
        tone_num = round(tone_heuristic.get_tone(num_interrupts) * (len(TONES) - 1))
        tone = synthesizer.generate_constant_wave(TONES[tone_num], SLEEP_TIME)

        print(tone_num, num_interrupts)
        queue.put(tone)


def consumer(queue):
    player = Player()
    player.open_stream()

    while True:
        tone = queue.get()

        if tone is None:
            break

        player.play_wave(tone)


def threaded_runner(tone_heuristic):
    queue = Queue(maxsize=1)

    t = Thread(target=consumer, args=[queue])
    t.start()

    try:
        producer(queue, tone_heuristic)
    except KeyboardInterrupt:
        queue.put(None)
        t.join()
        print('closing...')

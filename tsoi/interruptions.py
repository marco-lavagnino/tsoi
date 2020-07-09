"""
In this module, the file /proc/interrupts is parsed
to get different values.
"""

INTERRUPTS_FILE = '/proc/interrupts'


def get_number_of_cores():
    """
    There are numerous ways of measuring number of cores.
    Some make the distinction between phisical cores and
    virtual ones.
    Since we only care about cores in this file, we'll get
    the number of cores from this file.
    """
    with open(INTERRUPTS_FILE) as f:
        line = f.readline()

    return len(line.split())


NUMBER_OF_CORES = get_number_of_cores()


def get_interruptions(interrupts_fileobj):
    """
    The file in /proc/interrupts displays the number of
    interrupts for various types since the system booted.
    This function sums them all into a single integer.
    """
    interruptions = 0

    contents = interrupts_fileobj.read()
    interrupts_fileobj.seek(0)

    for line in contents.split('\n')[1:]:
        columns = line.split()
        if len(columns) < NUMBER_OF_CORES + 1:
            continue

        interruptions += sum(int(n) for n in columns[1:NUMBER_OF_CORES + 1])

    return interruptions


def interruption_iter():
    """
    A generator that returns the amount of interruptions
    that happened since the last time a value was consumed.
    """
    with open(INTERRUPTS_FILE) as f:
        last_interruptions = get_interruptions(f)

        while True:
            current_interruptions = get_interruptions(f)
            yield current_interruptions - last_interruptions
            last_interruptions = current_interruptions

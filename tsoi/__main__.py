from docopt import docopt
from tone_heuristics import HEURISTIC_OPTIONS
from runner import threaded_runner

if __name__ == '__main__':
    options = "|".join(HEURISTIC_OPTIONS.keys())

    cli_help = f"Usage: tsoi [{options}]"

    arguments = docopt(cli_help, version='TSOI 1.0')

    for name, heuristic_class in HEURISTIC_OPTIONS.items():
        if arguments[name]:
            heuristic = heuristic_class()

    threaded_runner(heuristic)

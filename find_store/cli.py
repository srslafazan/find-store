"""
find_store

Usage:
  find_store hello
  find_store -h | --help
  find_store --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  find_store hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/srslafazan/find_store-cli
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))

from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION

def main():
    """ Main CLI entrypoint. """
    import commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.items():
        if hasattr(commands, k):
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()

if __name__ == '__main__':
  main()

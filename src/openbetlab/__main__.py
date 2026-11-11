"""Lets you run ``python -m openbetlab`` instead of the ``openbetlab`` command."""

import sys

from openbetlab.cli import main

# The guard stops the CLI from running when this file is merely imported
# (for example by test tools), rather than executed with ``python -m``.
if __name__ == "__main__":
    sys.exit(main())

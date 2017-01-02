#!/usr/bin/env python
import os

# This is just a helper script to get the current directory, since we can't
# do that reliably with bash.
print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

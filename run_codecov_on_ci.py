#!/usr/bin/env python
"""Runs `codecov --token=$1` only if `CI=true` environment variable is set."""

import os
import sys

if __name__ == "__main__":
    if os.environ.get("CI", "").lower() == "true":
        os.system("codecov --token=%s" % sys.argv[1])

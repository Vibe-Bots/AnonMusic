# Copyright (c) 2026 Vibe-Bots
# Open-sourced under MIT terms.
# Included within AnonMusic framework.


import os

from ..logging import LOGGER


def dirr():
    for file in os.listdir():
        if file.endswith((".jpg", ".jpeg", ".png")):
            os.remove(file)

    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    if "cache" not in os.listdir():
        os.mkdir("cache")

    LOGGER(__name__).info("All Directories Loaded.")

# -*- coding: UTF-8 -*-
"""
Unit tests.

We are going to use PIL to load an image into a list creating a predictable memory leak.
"""
import os
from pathlib import Path
from PIL import Image
from razortrace import Probe, probe


HERE = os.path.abspath(os.path.dirname(__file__))
IMG = Path(HERE + '/lightbulb.png')
HOLD = None


class Leak:
    """
    An attempt to create a predictable memory leak.
    """
    images = list()

    def __init__(self):
        self.probe = Probe(HERE)

    def load(self, count: int = 10):
        """
        This will loop for the number specified in ``count`` loading our test image each time.
        param count: Number of times to iterate.
        """
        self.probe.sample()
        while count:
            img = Image.open(IMG)
            img = img.load()
            self.images.append(img)
            count -= 1
        self.probe.sample()
        self.probe.report(traceback=True, debug=True)
        return self


LEAK = Leak()


def test_image():
    """
    This will test for an image memory leak.
    """
    global HOLD
    global LEAK
    HOLD = LEAK.load(1000)
    assert len(HOLD.probe.filtered_statistics) == 3
    HOLD.images = None
    HOLD.probe.clear()
    HOLD = None
    del LEAK


@probe(traceback=True, debug=True)
def text():
    """
    Creates a memory leak from a text file.
    """
    global HOLD
    HOLD = list()
    with open(Path(HERE + '/text.txt'), "r") as txt:
        for line in txt.readlines():
            HOLD.append(line)
    for cycle in range(0, 1000):
        HOLD.append([cycle, HOLD])
    return


def test_text():
    """
    Fires off the above logic into a unit test.
    """
    txt = text()
    assert len(txt.trace.filtered_statistics) == 9

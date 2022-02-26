# -*- coding: UTF-8 -*-
"""
Unit tests.

We are going to use PIL to load an image into a list creating a predictable memory leak.
"""
import os
from pathlib import Path
from PIL import Image
from razortrace import Probe


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
        :param count: Number of times to iterate.
        """
        self.probe.sample()
        while count:
            img = Image.open(IMG)
            img = img.load()
            self.images.append(img)
            count -= 1
        self.probe.sample()
        self.probe.report(traceback=True, debug=True)
        # self.probe.comp_n_show(6)
        return self


LEAK = Leak()


def test_basic():
    """
    This will test for a basic memory leak.
    """
    global HOLD
    HOLD = LEAK.load(1000)
    assert len(HOLD.probe.filtered_statistics) == 3

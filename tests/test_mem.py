# -*- coding: UTF-8 -*-
"""
Unit tests.

We are going to use PIL to load an image into a list creating a predictable memory leak.
"""
import os
from pathlib import Path
from PIL import Image  # noqa
from razortrace import Probe, probe


HERE = os.path.abspath(os.path.dirname(__file__))
IMG = Path(HERE + '/lightbulb.png')
HOLD = list()


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
        self.probe.sample()  # <--- Leak ---------------------------------------------
        while count:
            img = Image.open(IMG)  # <--- Leak ---------------------------------------------
            self.images.append(img)
            count -= 1
        self.probe.sample()  # <--- Leak ---------------------------------------------
        self.probe.report(traceback=True, debug=True)
        del img
        return self.probe.filtered_statistics

    def clear(self):
        """
        Purges our memory.
        """
        self.probe.reset()
        for idx, image in enumerate(self.images):
            image.close()
            self.images[idx] = None


def test_image():
    """
    This will test for an image memory leak.
    """
    leak = Leak()
    stats = list(leak.load(1000))
    leak.clear()
    del leak
    lines = list()
    for stat in stats:
        lines.append(stat['line'])
    assert lines == [37, 35, 40]


@probe(trigger='TRACE_TEXT', traceback=True, clear=True, debug=True)
def text():
    """
    Creates a memory leak from a text file.
    """
    global HOLD
    with open(Path(HERE + '/text.txt'), "r") as txt:  # <--- Leak ---------------------------------------------
        for line in txt.readlines():  # <--- Leak ---------------------------------------------
            HOLD.append(line)
    for cycle in range(0, 1000):
        HOLD.append([cycle, HOLD])
    return


def test_text():
    """
    Fires off the above logic into a unit test.
    """
    os.environ["TRACE_TEXT"] = "1"  # Enable trace.
    txt = text()  # <--- Leak ---------------------------------------------
    stats = txt.trace.filtered_statistics
    txt.trace.reset()
    lines = list()
    for stat in stats:
        lines.append(stat['line'])
    assert lines == [76, 75]


def test_disable():
    """
    As the trace was disabled in the last test, this will confirm that we are properly cleaning up
    when not in use.
    """
    os.environ.pop("TRACE_TEXT")  # Disable trace so we can confirm cleanup works.
    txt = text()
    stats = txt.trace.filtered_statistics
    assert len(stats) == 0

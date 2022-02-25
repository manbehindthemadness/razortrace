# -*- coding: UTF-8 -*-
"""
One fancy-ass init file
"""

try:
    from main import MemTrace as Probe
except ImportError:
    from .main import MemTrace as Probe

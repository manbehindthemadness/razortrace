.. razortrace documentation master file, created by
   sphinx-quickstart on Sun Feb 27 09:24:31 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation: razortrace
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Home
------

https://github.com/manbehindthemadness/razortrace

Description
-----------

Razortrace is a memory diagnostic tool based on the ``tracemalloc`` library. It's aim is to provide rapid identification
of memory leaks and produce straightforward, human-readable reports.

Requirements
------------

The main library requires no additional packages; however, pytest and PIL are needed to run tests.

Usage
-----

Razor trace can be used as a decorator *(recommended)* or alternatively, as an
imported class *(useful for more specific scenarios)*. Leak detection is achieved by starting tracemalloc and
capturing a memory snapshot. Once arbitrary code has completed execution a second snapshot is taken and compared
against the first. Results are filtered based on two sets of criteria:

* Execution has been increasing in memory usage throughout the sampling process.
* Execution has not reclaimed any memory throughout the sampling process *(configurable)*.

When used as a decorator, each probe is activates by a trigger in the form of an environment variable.
This allows for many tests to be selectively placed throughout a project with minimal alteration of the business logic.

**Parameters**

* ``trigger`` An environment variable if returned ``True`` will enable the trace.
   * default - ``str()``
* ``traceback`` Specifies the inclusion of tracebacks in the final report.
   * default - ``False``
* ``clear`` If set ``True`` the memory trace will be cleared after each execution.
   * default - ``False``
* ``strict`` Shows only executions that have **not** reclaimed memory during the sampling process.
   * default - ``True``
* ``debug`` If set ``True`` the final report will include the memory samples recorded in the form of a ``list()`` in addition to allowing trace items from within the libraries folder structure.
   * default - ``False``
* ``here`` The current working directory *(only required when initializing the probe as a class)*.
   * default - root install directory

Examples
--------

code blocks and examples here...

Installation
------------

razortrace can be installed using pip:

``pip install razortrace``

or alternatively:

.. code-block:: sh

   git clone https://github.com/manbehindthemadness/razortrace.git
   cd razortrace
   python setup.py install



Disclaimer
----------

This library is still in development, please use at your own risk and test sufficiently before using it in a
production environment.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

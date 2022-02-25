# -*- coding: UTF-8 -*-
"""
This is a memory tracing utility designed to find memory leaks.

https://www.fugue.co/blog/diagnosing-and-fixing-memory-leaks-in-python.html
"""
import gc
import os
import linecache
import tracemalloc


def display_top(snapshot, key_type='lineno', limit=100):
    """
    From the documentation.
    """
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print("#%s: %s:%s: %.1f KiB" % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('LINE    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


class MemTrace:
    """
    An easy way to call tracemalloc
    """
    runner = 0
    here = os.path.abspath(os.path.dirname(__file__))
    statistics = dict()
    filtered_statistics = list()

    def __init__(self, here: [str, None] = None):
        self.snapshots = list()
        if here:
            self.here = str(here)
        tracemalloc.start(10)

    def take_snap(self):
        """
        This will take a memory snapshot.
        """
        snapshot = tracemalloc.take_snapshot()
        self.snapshots.append(snapshot)
        return snapshot

    def comp_snap(self, ln: int = 100, pattern: str = '*ImageTk*', comp: str = 'filename'):
        """
        This will compare the passed snap with the one specified in memory.
        """
        filters = [tracemalloc.Filter(inclusive=True, filename_pattern=pattern)]

        if len(self.snapshots) > 1:
            filtered_stats = self.snapshots[-1].filter_traces(filters).compare_to(self.snapshots[-2], comp)
            self.show_stats(filtered_stats, ln)
        return self

    def show_snap(self, ln: int = 100):
        """
        This will pretty print a snapshot.
        """
        display_top(self.snapshots[-1], 'filename', ln)
        return self

    @staticmethod
    def cleanup():
        """
        This fires off the garbage collection and clears the caches to prevent false positives.
        :return:
        """
        gc.collect()
        linecache.clearcache()  # This is experimental.

    @staticmethod
    def show_stats(stats, ln: int = 100):
        """
        This will print the stats from a series of filtered staps.
        """
        for stat in stats[:ln]:
            print("{} new KiB {} total KiB {} new {} total memory blocks: ".format(stat.size_diff / 1024,
                                                                                   stat.size / 1024, stat.count_diff,
                                                                                   stat.count))

            for line in stat.traceback.format():
                print(line)

    def comp_n_show(self, ln: int = 100):
        """
        THis will take a snap and compare it with the last.
        """
        self.cleanup()
        if not self.runner % 50:
            print('trace:' + str(self.runner), '------------------------------------------------------------------')
            self.take_snap()
            self.show_snap(ln)
            self.comp_snap(ln)
            print('--------------------------------TRACEBACK---------------------------------')
            self.comp_snap(ln, comp='traceback')
            # self.show_snap(ln)
            print('-----------------------------------END------------------------------------')
            pass
        self.runner += 1
        if not self.runner % 10:
            print(self.runner)
        return self

    def sample(self):
        """
        This will take a memory snapshot and save it into history.
        """
        self.take_snap()

    def report(self, traceback: bool = False):
        """
        This is some memory handling logic we are using to prevent memory leaks.
        """
        filters = [
            tracemalloc.Filter(False, "<frozen importlib._bootstrap>", all_frames=True),
            tracemalloc.Filter(False, "<frozen importlib._bootstrap_external>", all_frames=True),
            tracemalloc.Filter(False, "<unknown>", all_frames=True),
        ]
        self.cleanup()
        print('\n=============================== leaks detected ===============================\n')
        filtered_stats = self.snapshots[-1].filter_traces(filters).compare_to(self.snapshots[-2], 'traceback')
        for i, d in enumerate(filtered_stats):
            for tb in d.traceback:
                match = tb.filename
                if self.here in match:
                    line = linecache.getline(tb.filename, tb.lineno).strip()
                    key = tb.filename + str(tb.lineno)
                    kb = d.size / 1024
                    if key in self.statistics.keys():
                        self.statistics[key]['sizes'].append(kb)
                    else:
                        self.statistics[key] = {
                            'line': tb.lineno,
                            'file': tb.filename,
                            'command': line,
                            'sizes': [kb],
                            'traceback': d.traceback
                        }
        for i, statistic in enumerate(self.statistics):
            stat = self.statistics[statistic]
            sizes = list(stat['sizes'])
            ordered_sizes = list(stat['sizes'])
            ordered_sizes.sort()
            ordered_sizes.reverse()
            if not sizes.count(sizes[0]) == len(sizes) and sizes == ordered_sizes:
                total = max(sizes)
                average = sum(sizes) / len(sizes)
                print(
                    i, stat['file'],
                    'line:', stat['line'],
                    'command:', stat['command'],
                    'average:', average,
                    'total kb', total,
                    '\n'
                )
                if traceback:
                    print('\t\t\t-----trace-----\n')
                    for line in stat['traceback']:
                        print(line)
                    print('\n')
                self.filtered_statistics.append(stat)
        return self

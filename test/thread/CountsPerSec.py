from datetime import datetime

class CountsPerSec:


    def __init__(self):

        self.start_time = None
        self._num_occurences = 0

    def start(self):
        self._start_time = datetime.now()
        self._num_occurences = 0

    def increment(self):
        self._num_occurences += 1

    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        return self._num_occurences / elapsed_time
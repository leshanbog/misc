from collections import defaultdict
import time


class TimeLogger:
    def __init__(self):
        self._section_to_time = defaultdict(float)
        self._latest_start_time = defaultdict(float)
        self._recursive_counter = defaultdict(int)

    def start_section(self, name: str):
        self._recursive_counter[name] += 1
        if name not in self._latest_start_time:
            self._latest_start_time[name] = time.perf_counter()

    def end_section(self, name: str):
        if name not in self._recursive_counter:
            raise ValueError('This section was not started!')

        self._recursive_counter[name] -= 1

        if self._recursive_counter[name] == 0:
            self._section_to_time[name] += time.perf_counter() - self._latest_start_time[name]
            del self._recursive_counter[name]
            del self._latest_start_time[name]

    def get_measurements(self):
        return self._section_to_time

    def zero_all_measurements(self):
        if len(self._recursive_counter) > 0:
            raise RuntimeError('There are exist not ended sections!')
        self._section_to_time = defaultdict(float)
        self._latest_start_time = defaultdict(float)
        self._recursive_counter = defaultdict(int)



TIME_LOGGER = TimeLogger()


def get_time_logger_results():
    return TIME_LOGGER.get_measurements()


def log_time(func):
    def wrapper(*args, **kwargs):
        TIME_LOGGER.start_section(func.__name__)
        res = func(*args, **kwargs)
        TIME_LOGGER.end_section(func.__name__)
        return res

    return wrapper


class TimeLog():
    def __init__(self, section_name):
        self.section_name = section_name

    def __enter__(self):
        TIME_LOGGER.start_section(self.section_name)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        TIME_LOGGER.end_section(self.section_name)

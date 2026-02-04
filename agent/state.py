from collections import deque


class RollingWindow:
    def __init__(self, size):
        self.size = size
        self._values = deque(maxlen=size)

    def add(self, value):
        self._values.append(value)

    def full(self):
        return len(self._values) == self.size

    def all_at_or_above(self, threshold):
        if not self.full():
            return False
        return all(v >= threshold for v in self._values)

    def all_at_or_below(self, threshold):
        if not self.full():
            return False
        return all(v <= threshold for v in self._values)

from typing import Generic, TypeVar

T = TypeVar("T")


class BoundedDropQueue(Generic[T]):
    """
    This class maintains at most max_size items in a list.
    When a new item is added, we remove the oldest item, to make space for the new item.
    """

    def __init__(self, max_size: int):
        self._max_size = max_size
        self._data: list[T] = []

    def append(self, item: T):
        for _ in range(0, len(self._data) - self._max_size + 1):
            self._data.pop(0)
        self._data.append(item)

    def resize(self, max_size: int):
        if max_size < self._max_size:
            self._data = self._data[-max_size:]
        self._max_size = max_size

    def __repr__(self) -> str:
        return f"BoundedDropQueue(max_size={self._max_size})"

    @property
    def data(self):
        return self._data[:]
